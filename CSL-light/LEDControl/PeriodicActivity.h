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

#include "IActivity.h"

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

enum SecondaryType
{
        kNo = 0,
        kAligned = 1,
        kInverted = 2
};

class PeriodicActivity : public IActivity
{
public:
        
protected:
        int32_t offset_;
        int32_t period_;
        int32_t duration_;
        int32_t duration_on_;
        int32_t duration_off_;
        uint8_t secondary_;
        bool on_;
        int32_t next_event_;
        
public:

        PeriodicActivity(int32_t start_offset_ms, int32_t period,
                         int32_t duration, uint8_t secondary)
                : offset_(start_offset_ms),
                  period_(period),
                  duration_(duration),
                  secondary_(secondary),
                  on_(false) {
                next_event_ = offset_;
                duration_on_ = duration;
                duration_off_ = period_ - duration;
                
                // SerialUSB.print("init: offset ");
                // SerialUSB.print(offset_);
                // SerialUSB.print(" period ");
                // SerialUSB.print(period_);
                // SerialUSB.print(" duration_on ");
                // SerialUSB.print(duration_on_);
                // SerialUSB.print(" duration_off ");
                // SerialUSB.print(duration_off_);
                // SerialUSB.print(" next ");
                // SerialUSB.println(next_event_);
        }
        
        virtual ~PeriodicActivity() = default;

        void start() override {
                if (duration_off_ == 0) {
                        on();
                        next_event_ = 0x7fffffff;
                } else if (duration_on_ == 0) {
                        off();
                        next_event_ = 0x7fffffff;
                }
        }
        
        void stop() override {}

        bool isOn() {
                return on_;
        }

        uint8_t isSecondary() {
                return secondary_;
        }

        void update(int32_t ms) {
                if (ms >= next_event_) {
                        on_ = !on_;
                        if (on_ == false) {
                                off();
                                next_event_ += duration_off_;
                        } else {
                                on();
                                next_event_ += duration_on_;
                        }
                }
        }
};
        
#endif // __PeriodicActivity_h
