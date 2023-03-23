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

#ifndef ROMI_ROVER_BUILD_AND_TEST_ACTIVITYMANAGER_H
#define ROMI_ROVER_BUILD_AND_TEST_ACTIVITYMANAGER_H

#include "PeriodicActivity.h"

#define MAX_ACTIVITIES 10

class ActivityManager
{
public:
    explicit ActivityManager();
    virtual ~ActivityManager();
    bool AddDigitalPulse(int32_t pin, int32_t start_delay_ms, int32_t duration, int32_t period, int32_t secondary, int32_t analog_value);
    bool AddprimaryDigitalPulse(int32_t pin, int32_t start_delay_ms, int32_t duration, int32_t period, int32_t secondary, int32_t analog_value);
    bool AddAnalogueMeasure(int32_t pin, int32_t start_delay_ms, int32_t duration, int32_t period, int32_t secondary);
    PeriodicActivity **Activities();

    uint8_t NumberActivities();

    void enable(bool enabled);
private:
    bool AddActivity(PeriodicActivity *activity);
private:
    PeriodicActivity *activities[MAX_ACTIVITIES];
    uint8_t current_number_activities;

};



#endif //ROMI_ROVER_BUILD_AND_TEST_ACTIVITYMANAGER_H
