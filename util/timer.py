# timer class that updates an optional dependent when it hits 0
class Timer:
    def __init__(this, time: float, start_max: bool, dependent: 'Dependent' = None):
        this.dependent = dependent
        
        this.default_time = time
        
        if start_max:
            this.time = time
        else:
            this.time = 0
        
    def countdown(this, dt) -> bool:
        if this.time > 0:
            this.time -= dt
            return False
        
        if not this.dependent == None:
            this.dependent.update()
        return True

    def reset(this, time = None):
        if time == None:
            this.time = this.default_time
        else:
            this.time = time

# dependent for a timer class that creates a timer to append to the list its passed
# override update() to do things
class Dependent:
    def __init__(this, time: int, timer_list: list[Timer]):
        depends_on = Timer(time, True)
        timer_list.append(depends_on)
        
    def update(this):
        pass