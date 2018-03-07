# RobotFactory
I have no idea what this is going to be but I am going to be playing with the theme of Little Worker Robots

### What I want to explore.
Task based agents are systems that I would like to explore a little.
Think Dwarf fortress. You do not have direct control of the agents
but you can create tasks that need to be done and the agents will
decide if they feel like doing it. This means that we cannot have
any kind of control of the agents. They live their lives and feel
compelled to do certain things.

### Game ideas.
1. The little robots are in a clergy and the player is god.
The Robo-monks go about their lives eating, drinking, sleeping and
worshipping. During the day or while they are sleeping, the robots
can have visions and dreams giving them a special task to do.
2. The little robots are in a guild of sorts and the tasks
that the user can give the robots are in the form of missions/quests
on a mission board.

### Technicalities.
1. Each agent is independent. They have needs (e.i tamagochi.
Hunger, sleep, etc) and ways to fulfill their needs.
2. The agents walk around and go about doing what needs to be done.
3. Player interaction is through tasks given to the agents indirectly.

### What needs to be created.
1. Independent agents with:
    * A needs system.
    * A way of checking a list/Stack/Queue of tasks
    to see what needs to be done.
    * A way to go fill up their needs and a moods.
2. World in which they live.
3. Ways for the player to add tasks.
4. Make everything fit the theme of the game idea.

#### Independent Agent
**Base Class:** Position, movement functions, task getting, drawing
<br>
**Each agent:** Movement style <br>
<img src="https://github.com/FearlessClock/RobotFactory/raw/master/docs/Movement%20and%20brain.gif" alt="" width="300" height="300"><br>
<p>I want the movement to be free form but I don't want the creature to
move in straight lines to the target. I will need some kind of path finding
and so I will need so kind of graph in the levels. The level could have
a grid overlaying it and then movement can be calculated from that. The
agent will then have nodes that it has to move to making the movement
calculated and smooth.</p>
<p>The movement is done by taking the normalized vector between the target
and the position of the agent.</p>

**Agent brain:** <p>Each agent will have a brain consisting of a Finite
State Machine (FSM) A finite state machine is a design pattern that uses
a finite number of states to represent the different states the agent can
be in and defines transitions between the different states. Each state
has its own set of functions. The state also handles the transitions.
To do the transitions, the creature pushes states to a stack and when
a state is finished, he pops the state off and carries on with what it
was doing before leaving that state.</p>

**Clergy Robot states**
<p>A Clergy Robot has several states to simulate inteligence in the robot.
The Robot has 4 states at the moment. It can be either Roaming (Doing nothing
important), Eating, Sleeping or completing tasks that need to be done.
The idle state will be the roaming state and from there the robot can go
to any of the other states at its disposition. From the task state,
a Robot can go to the eating or sleeping state and then come back when
they are done.</p>
<img src="https://github.com/FearlessClock/RobotFactory/raw/master/docs/State%20Machine.png" alt="" width="300" height="300"><br>


**Points of Interest**
<p>The design idea behind PoIs are to facilitate the designation of places
of rest or places to eat or other important places on the map.
This will allow the AI to easily know where to go when in need of something
Each PoI can also be limited to 1 single person</p>

**Task lists**
<p>This is one of the more important parts of the project. The task list
is where the tasks created by the player will be put and also where
automatic task will be put. The AI will then go and look in this list to
find a task that it wants to do. </p>

**Timed Events**
<p>Timed events are not event based but rather are called when the time
allocated to each "Event" arrives. By using this, I will be able to
schedule tasks to run at a certain time in the game. (e.i make a Clergy
 go preach to the congregation every 2h)</p>

**Game style**
<p>My art isn't good but it works. I made some "Real" art for the tileset
and it makes the game look a lot better. The AI still doesn't have its
own images but I will do that later</p>
<img src="https://github.com/FearlessClock/RobotFactory/raw/master/images/TileSheet.png" alt="" width="150" height="150"><br>

**Player**
<p></p>

**Human**
<p>A human is a dumb creature that just has a single decorative task in
the game. In the first iteration, they are the people coming to the
robot service. They are very simple, being able to just be spawned,
go to a spot, wait for a task to be finished then leave and disappear.
The also have a factory that easily creates them.</p>

**Dev Log**
<p>When the robot was going to spots on the map, the robot would stop
just before getting to the spot where I wanted him to go and I thought
it was a probleme with the AStar code but it was actaully to do with
how the robot was calculating its distance to the target. By converting
to grid space, the robot got into the grid the moment the top left corner
touched the square. I changed it to calculate the distance in world space,
and now it works much better.</p>
<p>I added a log of debugging and most notably of all is the pathfinding
debugging! Which is not only really useful but also cool to look at. </p>

<p>I fixed the pathing problem! When switching states from tasking to
eating/sleeping, the pathing wasn't turned off and so the AI walked to
the last target before changing to a new target. I also realised that
the A* algorithm wasn't returning the whole path which made making the
AI walk to the last.</p>

<p>I added some humans for the congregation. I now have a concrete example
of how I want to use the examples and the humans. I have a task that is spawned
and at the same time I create a few humans that will go and sit in the church
and wait for the service to finish. When the task is finsihed, the robot
carries on with his life and the humans go away. I added some more debugging,
most noteworthy is the debug on the screen as an overlay.</p>

<p>The Robots now will not go to the same chair/bed when they look for a
PoI. Each PoI can be occupied and so will be used to check if someone is
already using it</p>

<p></p>
