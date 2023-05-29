#ifndef __Due_h
#define __Due_h

#include "IBoard.h"
#include "DueTimer.h"

class Due : public IBoard
{
protected:
        DueTimer timer_;
public:
        Due();
        ~Due() override = default;
        ITimer& get_timer() override;
};
        
#endif // __Due_h

