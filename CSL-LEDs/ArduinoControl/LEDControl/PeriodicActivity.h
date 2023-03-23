/*
  
  Copyright (C) 2022 Sony Computer Science Laboratories
  
  Author(s) Peter Hanappe, Douglas Boari, Aliénor Lahlou
  
  free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  
  This program is distributed in the hope that it will be useful, but
  WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  General Public License for more details.
  
  You should have received a copy of the GNU General Public License
  along with this program.  If not, see
  <http://www.gnu.org/licenses/>.
  
 */

#ifndef __PeriodicActivity_h
#define __PeriodicActivity_h

#include <stdint.h>
// For testing without arduino.
//#define OUTPUT 0
//#define HIGH 0
//#define LOW 1
//
//static void pinMode(uint16_t pin, uint16_t fn)
//{
//}
//
//static void digitalWrite(uint16_t pin, uint16_t fn)
//{
//}
//
//static uint16_t analogRead(uint16_t pin)
//{
//    return pin;
//}

class PeriodicActivity
{
public:
        int32_t offset;
        int32_t period;
        int32_t duration;
        int32_t duration_on;
        int32_t duration_off;
        int32_t secondary;
        bool state;
        int32_t next_event;
        int32_t enabled;
        
        PeriodicActivity(int32_t start_offset_ms, int32_t period, int32_t duration, int32_t secondary)
                : offset(start_offset_ms), period(period), duration(duration), secondary(secondary), state(false), enabled(true) {
                next_event = offset;
                duration_on = duration;
                duration_off = period - duration;
        }
        
        virtual ~PeriodicActivity() = default;

        void enable() {
                enabled = true;
        }

        void disable() {
                enabled = false;
        }

        bool is_enabled() {
                return enabled;
        }

        int32_t is_secondary() {
            return secondary;
          }

        void update(int32_t ms) {
                if (ms >= next_event) {
                        state = !state;
                        if (state == false) {
                                off();
                                next_event += duration_off;
                        } else {
                                on();
                                next_event += duration_on;
                        }
                }
                if (state == true)
                        measure();
        }
        
        virtual void on() = 0;
        virtual void off() = 0;
        virtual void measure() = 0;
                
};

class DigitalPulse : public PeriodicActivity
{
public:
        int8_t pin;
        int32_t analog_value;
        DigitalPulse(int32_t pin_, int32_t start_offset_ms, int32_t period, int32_t duration, int32_t secondary, int32_t analog_value_)
                : PeriodicActivity(start_offset_ms, period, duration, secondary), pin(pin_), analog_value(analog_value_) {
                pinMode(pin, OUTPUT);                
        }

        void on() override {
                analogWrite(pin, analog_value);
        }
        
        void off() override {
                analogWrite(pin, 0);
        }

        void measure() override {}
};



class primaryDigitalPulse : public PeriodicActivity
{
public:
        PeriodicActivity *secondary_activities[10];
        int8_t current_number_secondarys = 0;
        int8_t pin;
        int32_t analog_value;
        
        primaryDigitalPulse(int32_t pin_, int32_t start_offset_ms, int32_t period, int32_t duration, int32_t secondary, int32_t analog_value_)
                : PeriodicActivity(start_offset_ms, period, duration, secondary), pin(pin_), analog_value(analog_value_) {
                
                pinMode(pin, OUTPUT);                
        }

        bool Addsecondary(PeriodicActivity *newactivity)
        { 
              bool retval = false;
              if (newactivity != nullptr)
              {
                    secondary_activities[current_number_secondarys++] = newactivity;
                    retval = true;
                }
                 return retval;
          
        }
        
        void on() override {

                for (int i = 0; i < current_number_secondarys; i++)
                {
                     if(secondary_activities[i]->is_secondary() == 1){
                        secondary_activities[i]->off();
                        }
                     else if(secondary_activities[i]->state && secondary_activities[i]->is_enabled())
                        {
                            secondary_activities[i]->on();
                        } 
                }
                digitalWrite(pin, analog_value);        
        }
        
        void off() override {
                digitalWrite(pin, 0);
                for (int i = 0; i < current_number_secondarys; i++)
                {
                        if(secondary_activities[i]->is_secondary() == 2){
                        secondary_activities[i]->off();
                        }
                        else if(secondary_activities[i]->state && secondary_activities[i]->is_enabled())
                        {
                            secondary_activities[i]->on();
                        } 
                }
              
        }

        void measure() override {}        

};
        
class AnalogMeasure : public PeriodicActivity
{
public:
        int8_t pin;
        
        int values[256];
        int current_value;
        int max_values;
        
        AnalogMeasure(int32_t pin_,  int32_t start_offset_ms, int32_t period, int32_t duration, int32_t secondary)
                : PeriodicActivity(start_offset_ms, period, duration, secondary), pin(pin_) {
                max_values = duration;
                if (max_values > 256)
                        max_values = 256;
        }

        void on() override {
                current_value = 0;
        }
        
        void off() override {
                if (current_value > 0) {
                        int sum = 0;
                        for (int i = 0; i < current_value; i++) {
                                sum += values[i];
                        }
                        sum /= current_value;
                }
        }

        void measure() override {
                if (current_value < max_values) {
                        values[current_value++] = analogRead(pin);
                }
        }
};
        
#endif // __PeriodicActivity_h
