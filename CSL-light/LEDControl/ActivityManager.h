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


//
// Created by douglas on 12/02/2021.
//

#ifndef __ActivityManager_h
#define __ActivityManager_h

#include "IActivity.h"

#define MAX_ACTIVITIES 10

class ActivityManager
{
private:
        IActivity *activities[MAX_ACTIVITIES];
        uint8_t current_number_activities;


public:
        explicit ActivityManager();
        virtual ~ActivityManager();
        
        bool addActivity(IActivity *activity);
        bool addDigitalPulse(int8_t pin, int32_t start_delay_ms, int32_t duration,
                             int32_t period, int8_t secondary
                             /*, int32_t analog_value*/);
        bool addPrimaryDigitalPulse(int8_t pin, int32_t start_delay_ms, int32_t duration,
                                    int32_t period, int8_t secondary
                                    /*, int32_t analog_value*/);
        bool addAnalogueMeasure(int8_t pin, int32_t start_delay_ms, int32_t duration,
                                int32_t period, int8_t secondary);
        IActivity **getActivities();

        uint8_t countActivities();
};

#endif //__ActivityManager_h
