#ifndef __DueTimer_h
#define __DueTimer_h

#include "ITimer.h"

class DueTimer : public ITimer
{
public:
        DueTimer();
        ~DueTimer() override = default;

        void init() override;
        void start(IActivity **a, int n) override;
        void stop() override;
};
        
#endif // __DueTimer_h

