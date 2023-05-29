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

#ifndef __PrimaryDigitalPulse_h
#define __PrimaryDigitalPulse_h

#include "PeriodicActivity.h"

class PrimaryDigitalPulse : public PeriodicActivity
{
protected:
        IActivity *secondary_activities_[10];
        int8_t number_secondaries_ = 0;
        int8_t pin_;
        //int32_t value_;
        
public:
        
        PrimaryDigitalPulse(int8_t pin, int32_t start_offset_ms, int32_t period,
                            int32_t duration, uint8_t secondary/*, int32_t value*/)
                : PeriodicActivity(start_offset_ms, period, duration, secondary),
                  pin_(pin)//,
                  /*value_(value)*/ {
                pinMode(pin_, OUTPUT);                
        }

        bool addSecondary(IActivity *newactivity)
        { 
              bool retval = false;
              if (newactivity != nullptr) {
                      secondary_activities_[number_secondaries_++] = newactivity;
                      retval = true;
              }
              return retval;
          
        }
        
        void on() override {
                on_ = true;
                digitalWrite(pin_, HIGH);        
                for (int i = 0; i < number_secondaries_; i++) {
                     if (secondary_activities_[i]->isSecondary() == 1) {
                             secondary_activities_[i]->off();
                     } else if (secondary_activities_[i]->isOn()) {
                             secondary_activities_[i]->on();
                     } 
                }
                //digitalWrite(pin_, value_);        
        }
        
        void off() override {
                //digitalWrite(pin_, 0);
                digitalWrite(pin_, LOW);        
                on_ = false;
                for (int i = 0; i < number_secondaries_; i++) {
                        if (secondary_activities_[i]->isSecondary() == 2){
                                secondary_activities_[i]->off();
                        } else if (secondary_activities_[i]->isOn()) {
                                secondary_activities_[i]->on();
                        } 
                }
        }
};

#endif // __PrimaryDigitalPulse_h
