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
**Each agent:** Movement style