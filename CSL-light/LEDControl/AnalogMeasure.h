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

#ifndef __AnalogMeasure_h
#define __AnalogMeasure_h

#include "PeriodicActivity.h"

class AnalogMeasure : public PeriodicActivity
{
public:
        int8_t pin;
        uint16_t values_[256];
        uint16_t current_index_;
        uint16_t max_index_;
        
        AnalogMeasure(int8_t pin_, int32_t start_offset_ms, int32_t period,
                      int32_t duration, uint8_t secondary)
                : PeriodicActivity(start_offset_ms, period, duration, secondary),
                  pin(pin_) {
                max_index_ = duration;
                if (max_index_ > 256)
                        max_index_ = 256;
        }

        void update(int32_t ms) {
                PeriodicActivity::update(ms);
                if (on_ == true) {
                        measure();
                }
        }
        
        void on() override {
                current_index_ = 0;
                on_ = true;
        }
        
        void off() override {
                on_ = false;
                if (current_index_ > 0) {
                        // int32_t sum = 0;
                        // for (uint16_t i = 0; i < current_index_; i++) {
                        //         sum += values_[i];
                        // }
                        // sum /= current_index_;
                }
        }

        void measure() {
                if (current_index_ < max_index_) {
                        values_[current_index_++] = analogRead(pin);
                }
        }
};

#endif // __AnalogMeasure_h
