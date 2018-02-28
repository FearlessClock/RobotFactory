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
![Alt Text](https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif)<br>
I want the movement to be free form but I don't want the creature to
move in straight lines to the target. I will need some kind of path finding
and so I will need so kind of graph in the levels. The level could have
a grid overlaying it and then movement can be calculated from that. The
agent will then have nodes that it has to move to making the movement
calculated and smooth.

**Agent brain:** Each agent will have a brain consisting of a Finite
State Machine (FSM) A finite state machine is a design pattern that uses
a finite number of states to represent the different states the agent can
be in and defines transitions between the different states. Each state
has its own set of functions. The state also handles the transitions.