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

#ifndef __DigitalPulse_h
#define __DigitalPulse_h

#include "PeriodicActivity.h"

class DigitalPulse : public PeriodicActivity
{
public:
        int8_t pin_;
        //int32_t value_;
        
        DigitalPulse(int8_t pin, int32_t start_offset_ms, int32_t period,
                     int32_t duration, uint8_t secondary/*, int32_t analog_value*/)
                : PeriodicActivity(start_offset_ms, period, duration, secondary),
                  pin_(pin)//,
                  /*value_(analog_value)*/ {
                pinMode(pin_, OUTPUT);                
        }

        void on() override {
                //analogWrite(pin_, value_);
                digitalWrite(pin_, HIGH);
                on_ = true;
        }
        
        void off() override {
                //analogWrite(pin_, 0);
                digitalWrite(pin_, LOW);
                on_ = false;
        }
};

#endif // __DigitalPulse_h
