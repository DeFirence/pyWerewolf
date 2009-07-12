#!/usr/bin/env python

from player import Role
from command_handler import Command

class Type:
    game        = 0     #messages relating to the game
    command     = 1     #messages relating to commands
    join        = 2     #messages relating to joining the game and the join command
    role        = 3     #messages relating to assigning the roles
    night       = 4     #messages relating to the night phase
    kill        = 5     #messages relating to the kill command
    see         = 6     #messages relating to the see command
    guard       = 7     #messages relating to the guard command
    day         = 8     #messages relating to the day phase
    vote        = 9     #messages relating to voting and the vote command
    die         = 10    #messages relating to players dying
    win         = 11    #messages relating to the winning of the game
    misc        = 12    #miscellaneous messages
    num         = 13    #num message types

    class Game:     #game type subtypes
        start           = 0 #message when a new game gets started
        started         = 1 #message when players tries to start game when one 
                            #is running alread
        join_starting   = 2 #message when player joins channel and game is in
                            #join phase
        join_running    = 3 #message when player joins channel and game is running
        join_none       = 4 #message when player joins channel and game is not running
        num             = 5 #num game subtypes

    class Command:  #command type subtypes
        unknown          = 0 #message when you enter an unknown command
        game_not_running = 1 #message when you enter a game command when a game
                             #isn't running
        num              = 2 #num command subtypes

    class Join:     #join type subtypes
        join    = 0 #message when you successfully join a game
        rejoin  = 1 #message when you try to join a game you already joined
        leave   = 2 #message when you leave a game in the joining phase
        nick    = 3 #message when you change your nick in joining phase
        ended   = 4 #message when you try to join when joining has ended
        end     = 5 #message when joining ends
        success = 6 #message when enough players have joined
        fail    = 7 #message when not enough players have joined
        num     = 8 #num join subtypes

    class Role:     #role type subtypes
        announce    = 0 #message to announce roles to players
        other       = 1 #message to tell other player of same role to player
        other_p     = 2 #same as above but plural
        count       = 3 #message to announce the number of each role
        count_p     = 4 #same as above but plural
        num         = 5 #num role subtypes

    class Night:    #night type subtypes
        first       = 0 #message when first night starts
        subsequent  = 1 #message when subsequent nights start
        task        = 2 #message to ask player to fullfil their task
        task_p      = 3 #same as above but plural
        num         = 4 #num night subtypes

    class Kill:     #kill type subtypes
        success         = 0 #message when kill command succeeds
        success_p       = 1 #same as above but plural
        not_night       = 2 #message when it's not night
        not_wolf        = 3 #message when you aren't a wolf
        invalid_format  = 4 #message when your kill command is invalidly formatted
        invalid_target  = 5 #message when your target isn't in the game
        invalid_target_wolf = 6 #message when your target is a wolf
        invalid_target_dead = 7 #message when your target is dead
        num             = 8 #num kill subtypes
        
    class See:      #see type subtypes
        success         = 0 #message when see command succeeds
        not_night       = 1 #message when it's not night
        not_seer        = 2 #message when you aren't a seer
        invalid_format  = 3 #message when your see command is invalidly formatted
        invalid_target  = 4 #message when your target isn't in the game
        invalid_target_dead = 5 #message when your target is dead
        result          = 6 #message to announce the result of your sightings
        num             = 7 #num see subtypes

    class Guard:    #guard type subtypes
        success         = 0 #message when guard command succeeds
        not_night       = 1 #message when it's not night
        not_guardian    = 2 #message when you aren't a guardian
        invalid_format  = 3 #message when your guard command is invalidly formatted
        invalid_target  = 4 #message when your target isn't in the game
        invalid_target_dead = 5 #message when your target is dead
        num             = 6 #num guard subtypes

    class Day:      #day type subtypes
        start   = 0 #message when day starts
        num     = 1 #num day subtypes
        
    class Vote:     #vote type subtypes
        start           = 0 #message when voting starts
        success         = 1 #message when vote command succeeds
        not_vote_time   = 2 #message when it's not voting time
        invalid_format  = 3 #message when yoru vote command is invalidly formatted
        invalid_target  = 4 #message when your target isn't in the game
        invalid_target_dead = 5 #message when your target is dead
        end             = 6 #message when voting ends
        tie             = 7 #message if there is a tie
        num             = 8 #num vote subtypes

    class Die:      #die type subtypes
        kill        = 0 #message to announce killing by wolves
        vote        = 1 #message to announce lynch killing
        not_voting  = 2 #message to announce death due to not voting for too many turns
        nick        = 3 #message to announce death due to nick change
        leave       = 4 #message to announce death due to leaving game
        num         = 5 #num die subtypes

    class Win:      #win type subtypes
        win         = 0 #message to announce the winning of a group
        win_p       = 1 #same as above but plural
        list_role   = 2 #message to announce player role
        list_role_p = 3 #same as above but plural
        num         = 4 #num win subtypes

    class Misc:     #misc type subtypes
        help        = 0 #message containing help information
        randplayer  = 1 #message to announce random player in game
        not_player  = 2 #message to tell user he's not in the game
        dead        = 3 #message to tell user he's dead
        num         = 4 #num misc subtypes
        
    #iterable list of types
    types = [(game, Game), (command, Command), (join, Join), (role, Role), 
             (night, Night), (kill, Kill), (see, See), (guard, Guard), 
             (day, Day), (vote, Vote), (die, Die), (win, Win), (misc, Misc)]

class MessageType:
    chan        = 0 #Message that will be sent to the channel
    notice_p    = 1 #Notice that will be sent to the player
    notice_c    = 2 #Notice that will be sent to the channel
    
class Theme:
    def __init__(self):
        #custom command names
        self.commands = [None for i in xrange(Commands.num)]

        #create 3D array to hold messages
        self.messages = [[[None for k in xrange(Role.num)] 
                         for j in xrange(subtype.num)] 
                         for i, subtype in Type.types]

        #Message format: -list of possible messages
        #                -each message is a list of lines
        #                -each line is 2-tuple where the first item is the type and 
        #                 second is the actual text

        ### MESSAGE TOKENS ###
        #TODO: add tokens for chan messages, pvt notices, chan notices and formatting
        #$bot is the name of the bot
        #$num is the number of times an action has been executed like join
        #$user gets replaced by the current user
        #$target gets replaced by who is targeted by current user
        #$votes gets replaced by current vote tallies
        #$roles gets the names of the roles
        #$alive gets the alive villagers

        ### GAME TOKENS ###
        #$user is the user who sent the command

        ### COMMAND TOKENS ###
        #$user is the user who sent the command
        #$target is the name of the command

        ### JOIN TOKENS ###
        #$user is the user who called the command
        #$num is the num players who have joined the game (so far)

        ### ROLE TOKENS ###
        #$user is the user who is recieving the message
        #$num is the number of players of that role

        ### NIGHT TOKENS ###
        #$bot is the name of the bot

        ### KILL $ SEE $ GUARD TOKENS ###
        #$user is the person issuing the command
        #$target is the target of the user's command
        
        ### DAY TOKENS ###
        #$num is the time left for talking
        
        ### VOTE TOKENS ###
        #$user is the person issuing the command
        #$target is the target of the user's command
        #$votes is the tally of the votes so far

        ### DIE TOKENS ###
        #$target is the target of the killing

        ### WIN TOKENS ###
        #$roles are the list of players with the perticular role

        ### MISC TOKENS ###
        #$user is person calling the command
        #$target is the result of the command

class WerewolfTheme(Theme):
    def __init__(self):
        Theme.__init__(self)
        self.commands[Command.start]        = "start"
        self.commands[Command.help]         = "help"
        self.commands[Command.join]         = "join"
        self.commands[Command.leave]        = "leave"
        self.commands[Command.kill]         = "kill"
        self.commands[Command.guard]        = "guard"
        self.commands[Command.see]          = "see"
        self.commands[Command.vote]         = "vote"
        self.commands[Command.randplayer]   = "randplayer"

        m   = self.messages #alias for messages
        t   = Type          #alias for Type
        r   = Role          #alias for Role
        mt  = MessageType   #alias for MessageType

        ### GAME MESSAGES ###
        m[t.game][r.Game.start][r.noone] = 
            [[(mt.chan, "$user started a new game! You have $num seconds to join!")]]
        m[t.game][r.Game.started][r.noone] = 
            [[(mt.notice_p, "A game already running. Join it if you still can!")]]
        m[t.game][r.Game.join_starting][r.noone] = 
            [[(mt.notice_p, "A game is starting. Type " + 
                            self.commands[Command.join] + " to join it.")]]
        m[t.game][r.Game.join_running][r.noone] = 
            [[(mt.notice_p, "A game is already running. It should finish soon, "+
                            "then you can join the fun. :)")]]
        m[t.game][r.Game.join_none][r.noone] = 
            [[(mt.notice_p, "No game is running. Start one by typing: !" + 
                            self.commands[Command.start])]]

        ### COMMAND MESSAGES ###
        m[t.command][r.Command.unknown][r.noone] = 
            [[(mt.notice_p, "$target is an invalid command. Type !" + 
                            self.commands[Command.help] + " for help")]]
        m[t.command][r.Command.game_not_running][r.noone] = 
            [[(mt.notice_p, "$target can only be used while a game is running. "+
                            "Start one by typing !" + self.commands[Command.start])]]

        ### JOIN MESSAGES ###
        m[t.join][r.Join.join][r.noone] = 
            [[(mt.chan, "$num. $user joined the hunt!")]]
        m[t.join][r.Join.rejoin][r.noone] =
            [[(mt.notice_p, "You have already joined the hunt.")]]
        m[t.join][r.Join.leave][r.noone] =
            [[(mt.chan, "$target has left the hunt.")]]
        m[t.join][r.Join.nick][r.noone] =
            [[(mt.chan, "$target has left the hunt.")]]
        m[t.join][r.Join.ended][r.noone] =
            [[(mt.notice_p, "Sorry the joining has ended.")]]
        m[t.join][r.Join.end][r.noone] =
            [[(mt.chan, "Joining ends.")]]
        m[t.join][r.Join.success][r.noone] =
            [[(mt.chan, "Congratulations, you have $num players in the hunt!")]]
        m[t.join][r.Join.fail][r.noone] =
            [[(mt.chan, "Sorry not enough players have joined.")]]
        
        ### ROLE MESSAGES ###
        m[t.role][r.Role.announce][r.villager] =
            [[(mt.notice_p, "You are a villager.")]]
        m[t.role][r.Role.announce][r.wolf] =
            [[(mt.notice_p, "You are a werewolf. rAwr!!!")]]
        m[t.role][r.Role.announce][r.seer] =
            [[(mt.notice_p, "You are a seer.")]]
        m[t.role][r.Role.announce][r.guardian] =
            [[(mt.notice_p, "You are a guardian.")]]
        m[t.role][r.Role.announce][r.angel] =
            [[(mt.notice_p, "You are an angel.")]]

        m[t.role][r.Role.other][r.wolf] =
            [[(mt.notice_p, "Your brethren is $wolves.")]]
        m[t.role][r.Role.other_p][r.wolf] =
            [[(mt.notice_p, "Your brethren are: $wolves")]]

        m[t.role][r.Role.count][r.villager] =
            [[(mt.chan, "There is $num villager.")]]
        m[t.role][r.Role.count][r.wolf] =
            [[(mt.chan, "There is $num werewolf.")]]
        m[t.role][r.Role.count][r.seer] =
            [[(mt.chan, "There is $num seer.")]]
        m[t.role][r.Role.count][r.guardian] =
            [[(mt.chan, "There is $num guardian.")]]
        m[t.role][r.Role.count][r.angel] =
            [[(mt.chan, "There is $num angel.")]]
        m[t.role][r.Role.count][r.traitor] =
            [[(mt.chan, "There is $num traitor.")]]

        m[t.role][r.Role.count_p][r.villager] =
            [[(mt.chan, "There are $num villagers.")]]
        m[t.role][r.Role.count_p][r.wolf] =
            [[(mt.chan, "There are $num werewolves.")]]
        m[t.role][r.Role.count_p][r.seer] =
            [[(mt.chan, "There are $num seers.")]]
        m[t.role][r.Role.count_p][r.guardian] =
            [[(mt.chan, "There are $num guardians.")]]
        m[t.role][r.Role.count_p][r.angel] =
            [[(mt.chan, "There are $num angels.")]]
        m[t.role][r.Role.count_p][r.traitor] =
            [[(mt.chan, "There are $num traitors.")]]

        ### NIGHT MESSAGES ###
        m[t.night][r.Night.first][r.noone] =
            [[(mt.chan, "Night descends over the unsuspecting village.")]]
        m[t.night][r.Night.subsequent][r.noone] =
            [[(mt.chan, "Villagers goes to an uneasy sleep.")]]
        
        m[t.night][r.Night.task][r.wolf] =
            [[(mt.chan, "Werewolf type: /msg $bot " + self.commands[Command.kill] + 
                        " <target> to kill. You have $num seconds.")]]
        m[t.night][r.Night.task][r.seer] =
            [[(mt.chan, "Seer type: /msg $bot " + self.commands[Command.see] + 
                        " <target> to see. You have $num seconds.")]]
        m[t.night][r.Night.task][r.guardian] =
            [[(mt.chan, "Guardian type: /msg $bot " + self.commands[Command.guard] + 
                        " <target> to guard. You have $num seconds.")]]

        m[t.night][r.Night.task_p][r.wolf] =
            [[(mt.chan, "Werewolves type: /msg $bot " + self.commands[Command.kill] + 
                        " <target> to kill. You have $num seconds.")]]
        m[t.night][r.Night.task_p][r.seer] =
            [[(mt.chan, "Seers type: /msg $bot " + self.commands[Command.see] + 
                        " <target> to see. You have $num seconds.")]]
        m[t.night][r.Night.task_p][r.guardian] =
            [[(mt.chan, "Guardians type: /msg $bot " + self.commands[Command.guard] + 
                        " <target> to guard. You have $num seconds.")]]

        ### KILL MESSAGES ###
        m[t.kill][r.Kill.success][r.noone] =
            [[(mt.notice_p, "You have selected $target for your feast.")]]
        m[t.kill][r.Kill.success_p][r.noone] =
            [[(mt.notice_p, "You have selected $target for your feast, but must "+
                            "wait for brethren to vote.")]]
        m[t.kill][r.Kill.not_night][r.noone] =
            [[(mt.notice_p, "You can only kill at night.")]]
        m[t.kill][r.Kill.not_wolf][r.noone] =
            [[(mt.notice_p, "You aren't a werewolf. Only werewolves can kill.")]]
        m[t.kill][r.Kill.invalid_format][r.noone] =
            [[(mt.notice_p, "Your " + self.commands[Command.kill] + 
                            " command was invalidly formated.")]]
        m[t.kill][r.Kill.invalid_target][r.noone] =
            [[(mt.notice_p, "$target isn't a player in the game.")]]
        m[t.kill][r.Kill.invalid_target_wolf][r.noone] =
            [[(mt.notice_p, "$target is one of your brethren you can't "+
                            "attack them.")]]
        m[t.kill][r.Kill.invalid_target_dead][r.noone] =
            [[(mt.notice_p, "$target is dead. You can't kill them twice.")]]

        ### SEE MESSAGES ###
        m[t.see][r.See.success][r.noone] =
            [[(mt.notice_p, "Your predictions will be revealed to you at dawn.")]]
        m[t.see][r.See.not_night][r.noone] =
            [[(mt.notice_p, "You can only see at night.")]]
        m[t.see][r.See.not_seer][r.noone] =
            [[(mt.notice_p, "You aren't a seer.")]]
        m[t.see][r.See.invalid_format][r.noone] =
            [[(mt.notice_p, "Your " + self.commands[Command.kill] + 
                            " command was invalidly formated.")]]
        m[t.see][r.See.invalid_target][r.noone] =
            [[(mt.notice_p, "$target isn't a player in the game.")]]
        m[t.see][r.See.invalid_target_dead][r.noone] =
            [[(mt.notice_p, "$target is dead. You don't need to see their "+
                            " true intentions.")]]

        m[t.see][r.See.result][r.villager] =
            [[(mt.notice_p, "$target is a villager.")]]
        m[t.see][r.See.result][r.wolf] =
            [[(mt.notice_p, "$target is a filthy werewolf.")]]
        m[t.see][r.See.result][r.seer] =
            [[(mt.notice_p, "$target is a seer.")]]
        m[t.see][r.See.result][r.guardian] =
            [[(mt.notice_p, "$target is a guardian.")]]
        m[t.see][r.See.result][r.angel] =
            [[(mt.notice_p, "$target is an angel.")]]

        ### GUARD MESSAGES ###
        m[t.guard][r.Guard.success][r.noone] =
            [[(mt.notice_p, "You have chosen to guard $target from werewolf "+
                            "attacks.")]]
        m[t.guard][r.Guard.not_night][r.noone] =
            [[(mt.notice_p, "You can only guard at night.")]]
        m[t.guard][r.Guard.not_guardian][r.noone] =
            [[(mt.notice_p, "You aren't a guardian.")]]
        m[t.guard][r.Guard.invalid_format][r.noone] =
            [[(mt.notice_p, "Your " + self.commands[Command.guard] + 
                            " command was invalidly formated.")]]
        m[t.guard][r.Guard.invalid_target][r.noone] =
            [[(mt.notice_p, "$target isn't a player in the game.")]]
        m[t.guard][r.Guard.invalid_target_dead][r.noone] =
            [[(mt.notice_p, "$target is dead. The dead don't need protection.")]]
        
        ### DAY MESSAGES ###
        m[t.day][r.Day.start][r.noone] =
            [[(mt.chan, "The villagers gather. You have $num seconds to "+
                        "make your accusations.")]]

        ### VOTE MESSAGES ###
        m[t.vote][r.Vote.start][r.noone] =
            [[(mt.chan, "Voting has started. Type: !"+ 
                        self.commands[Command.vote] + " <target> to vote for"+
                        "<target>. You have $num seconds to vote.")]]
        m[t.vote][r.Vote.success][r.noone] =
            [[(mt.chan, "$user voted for $target. ($votes)")]]
        m[t.vote][r.Vote.not_vote_time][r.noone] =
            [[(mt.notice_p, "Sorry you can only vote during voting time.")]]
        m[t.vote][r.Vote.invalid_format][r.noone] =
            [[(mt.notice_p, "Your " + self.commands[Command.vote] + 
                            " command was invalidly formated.")]]
        m[t.vote][r.Vote.invalid_target][r.noone] =
            [[(mt.notice_p, "$target isn't a player in the game.")]]
        m[t.vote][r.Vote.invalid_target_dead][r.noone] =
            [[(mt.notice_p, "$target is dead. You can't lynch the dead.")]]
        m[t.vote][r.Vote.end][r.noone] =
            [[(mt.chan, "Voting has ended. Tallying votes...")]]
        m[t.vote][r.Vote.tie][r.noone] =
            [[(mt.chan, "There was a tie, randomly choosing target.")]]

        ### DIE MESSAGES ###
        m[t.die][r.Die.kill][r.villager] =
            [[(mt.chan, "The villagers gather the next morning "+
                        "in the village center, but $target "+
                        "does not appear. The villagers "+
                        "converge on $target's home and find "+
                        "them decapitated in their bed. After "+
                        "carrying the body to the church, the "+
                        "villagers, now hysterical, return to "+
                        "the village center to decide how to "+
                        "retaliate..."),
              (mt.chan, "$target the villager was killed.")],

             [(mt.chan, "As some villagers begin to gather in "+
                        "the village center, a scream is "+
                        "heard from the direction of $target's "+
                        "house. The elderly villager who had "+
                        "screamed points to the fence, on top "+
                        "of which, the remains of $target are "+
                        "impaled, with their intestines "+
                        "spilling onto the cobbles. "+
                        "Apparently $target was trying to flee "+
                        "their attacker..."),
              (mt.chan, "$target the villager was killed.")],

             [(mt.chan, "When the villagers gather at the "+
                        "village center, one comes running from "+
                        "the hanging tree, screaming at others "+
                        "to follow. When they arrive at the "+
                        "hanging tree, a gentle creaking echoes "+
                        "through the air as the body of $target "+
                        "swings gently in the breeze, its arms "+
                        "ripped off at the shoulders. It appears "+
                        "the attacker was not without a sense of "+
                        "irony..."),
              (mt.chan, "$target the villager was killed.")],

             [(mt.chan, "As the village priest gathers the "+
                        "prayer books for the morning's sermon, "+
                        "he notices a trickle of blood snaking "+
                        "down the aisle. He looks upward "+
                        "to see $target impaled on the crucifix "+
                        "- the corpse has been gutted. He "+
                        "shouts for help, and the other "+
                        "villagers pile into the church and "+
                        "start arguing furiously..."),
              (mt.chan, "$target the villager was killed.")]]
        m[t.die][r.Die.kill][r.seer] =
            [[(mt.chan, "The first villager to arrive at the "+
                        "center shrieks in horror - lying on the "+
                        "cobbles is a blood stained Ouija Board, "+
                        "and atop it sits $target's head. It "+
                        "appears $target the Seer had been seeking "+
                        "the guidance of the spirits to root out "+
                        "the wolves, but apparently the magic "+
                        "eight ball didn't see THIS one coming..."),
              (mt.chan, "$target the seer was killed.")]]
        m[t.die][r.Die.kill][r.guardian] =
            [[(mt.chan, "As one of the villagers passes "+
                        "$target's home, he sees a bloody "+
                        "mess in front of the door. After "+
                        "following the trail of blood and gore, "+
                        "he finds $target's body torn to pieces "+
                        "with herbs and powder flung all about. "+
                        "It's too bad $target the Guardian was "+
                        "unable to ward off these evil beings..."),
              (mt.chan, "$target the guardian was killed.")]]
        m[t.die][r.Die.kill][r.noone] =
            [[(mt.chan, "The villagers gather the next morning in "+
                        "the village center, to sighs of relief - "+
                        "it appears there was no attack the "+
                        "previous night.")]]
        
        m[t.die][r.Die.vote][r.villager] =
            [[(mt.chan, "The air thick with adrenaline, the "+
                        "villagers grab $target who struggles "+
                        "furiously, pleading innocence, but "+
                        "the screams fall on deaf ears. "+
                        "$target is dragged to the stake at "+
                        "the edge of the village, and burned "+
                        "alive. But the villagers shouts and "+
                        "cheers fade as they realise the moon "+
                        "is already up - $target was not a "+
                        "werewolf after all..."),
              (mt.chan, "$target the villager was killed.")],

             [(mt.chan, "Realising the angry mob is turning, "+
                        "$target tries to run, but is quickly "+
                        "seized upon. $target is strung up to "+
                        "the hanging tree, and a hunter readies "+
                        "his rifle with a silver slug, as the "+
                        "block is kicked from beneath them. "+
                        "But there is a dull snap, and $target "+
                        "hangs, silent, motionless. The silent "+
                        "villagers quickly realise their grave "+
                        "mistake..."),
              (mt.chan, "$target the villager was killed.")]]
        m[t.die][r.Die.vote][r.wolf] =
            [[(mt.chan, "After coming to a decision, $target is "+
                        "quickly dragged from the crowd and "+
                        "dragged to the hanging tree. $target is "+
                        "strung up, and the block kicked from "+
                        "beneath their feet. There is a yelp of "+
                        "pain, but $target's neck doesn't snap, "+
                        "and fur begins to sprout from his/her "+
                        "body. A gunshot rings out, as a "+
                        "villager puts a silver bullet in the "+
                        "beast's head..."),
              (mt.chan, "$target the werewolf was killed.")]]
        m[t.die][r.Die.vote][r.seer] =
            [[(mt.chan, "$target runs before the mob is organised, "+
                        "dashing away from the village. Tackled to "+
                        "the ground near the lake, $target is tied "+
                        "to a log, screaming, thrown into the water. "+
                        "With no means of escape, $target the Seer "+
                        "drowns, but as the villagers watch, cards "+
                        "float to the surface and their mistake "+
                        "is all too apparent..."),
              (mt.chan, "$target the seer was killed.")]]
        m[t.die][r.Die.vote][r.guardian] =
            [[(mt.chan, "$target runs before the mob is "+ 
                        "organised, running for the safety "+
                        "of home. Just before reaching home, "+
                        "$target is hit with a large stone, "+
                        "then another. With no means of escape, "+
                        "$target is stoned to death, his body "+
                        "crushed. One curious villager enters "+
                        "the house to find proof that $target "+
                        "was a Guardian after all..."),
              (mt.chan, "$target the guardian was killed.")]]
        m[t.die][r.Die.vote][r.angel] =
            [[(mt.chan, "$target the angel is killed by the angry mob."),
              (mt.chan, "$target the angel was killed.")]]
        m[t.die][r.Die.vote][r.noone] =
            [[(mt.chan, "Noone was voted for. The good thingies "+
                        "will not be happy")]]
        
        m[t.die][r.Die.not_voting][r.villager] =
            [[(mt.chan, "$target the villager died for defying "+
                        "the good."),
              (mt.chan, "$target the villager has died.")]]
        m[t.die][r.Die.not_voting][r.wolf] =
            [[(mt.chan, "$target the werewolf died for defying "+
                        "the good."),
              (mt.chan, "$target the werewolf has died.")]]
        m[t.die][r.Die.not_voting][r.seer] =
            [[(mt.chan, "$target the seer died for defying "+
                        "the good."),
              (mt.chan, "$target the seer has died.")]]
        m[t.die][r.Die.not_voting][r.guardian] =
            [[(mt.chan, "$target the guardian died for "+
                        "defying the good."),
              (mt.chan, "$target the guardian has died.")]]
        m[t.die][r.Die.not_voting][r.angel] =
            [[(mt.chan, "$target the angel died for defying "+
                        "the good."),
              (mt.chan, "$target the angel has died.")]]
        
        m[t.die][r.Die.nick][r.villager] =
            [[(mt.chan, "$target the villager got killed for "+
                        "changing nicks."),
              (mt.chan, "$target the villager has died.")]]
        m[t.die][r.Die.nick][r.wolf] =
            [[(mt.chan, "$target the werewolf got killed for changing "+
                        "nicks."),
              (mt.chan, "$target the werewolf has died.")]]
        m[t.die][r.Die.nick][r.seer] =
            [[(mt.chan, "$target the seer got killed for changing "+
                        "nicks."),
              (mt.chan, "$target the seer has died.")]]
        m[t.die][r.Die.nick][r.guardian] =
            [[(mt.chan, "$target the guardian got killed for "+
                        "changing nicks."),
              (mt.chan, "$target the guardian has died.")]]
        m[t.die][r.Die.nick][r.angel] =
            [[(mt.chan, "$target the angel got killed for changing "+
                        "nicks."),
              (mt.chan, "$target the angel has died.")]]
        
        m[t.die][r.Die.leave][r.villager] =
            [[(mt.chan, "$target the villager got killed for "+
                        "leaving the game."),
              (mt.chan, "$target the villager has died.")]]
        m[t.die][r.Die.leave][r.wolf] =
            [[(mt.chan, "$target the werewolf got killed for "+
                        "leaving the game."),
              (mt.chan, "$target the werewolf has died.")]]
        m[t.die][r.Die.leave][r.seer] =
            [[(mt.chan, "$target the seer got killed for leaving "+
                        "the game."),
              (mt.chan, "$target the seer has died.")]]
        m[t.die][r.Die.leave][r.guardian] =
            [[(mt.chan, "$target the guardian got killed for "+
                        "leaving the game."),
              (mt.chan, "$target the guardian has died.")]]
        m[t.die][r.Die.leave][r.angel] =
            [[(mt.chan, "$target the angel got killed for "+
                        "leaving the game."),
              (mt.chan, "$target the angel has died.")]]
        
        ### WIN MESSAGES ###
        m[t.win][r.Win.win][r.wolf] =
            [[(mt.chan, "The werewolf has won.")]]
        m[t.win][r.Win.win_p][r.wolf] =
            [[(mt.chan, "The werewolves have won.")]]
        m[t.win][r.Win.win][r.villager] =
            [[(mt.chan, "The villager has won.")]]
        m[t.win][r.Win.win_p][r.village] =
            [[(mt.chan, "The villagers have won.")]]
        m[t.win][r.Win.win][r.noone] =
            [[(mt.chan, "No one is left alive. The town is desolate. "+
                        "The game ends in adraw.")]]
        
        m[t.win][r.Win.list_role][r.villager] =
            [[(mt.chan, "The villager was: $roles")]]
        m[t.win][r.Win.list_role][r.wolf] =
            [[(mt.chan, "The werewolf was: $roles")]]
        m[t.win][r.Win.list_role][r.seer] =
            [[(mt.chan, "The seer was: $roles")]]
        m[t.win][r.Win.list_role][r.guardian] =
            [[(mt.chan, "The guardian was: $roles")]]
        m[t.win][r.Win.list_role][r.angel] =
            [[(mt.chan, "The angel was: $roles")]]
        m[t.win][r.Win.list_role][r.traitor] =
            [[(mt.chan, "The traitor was: $roles")]]

        m[t.win][r.Win.list_role_p][r.villager] =
            [[(mt.chan, "The villagers were: $roles")]]
        m[t.win][r.Win.list_role_p][r.wolf] =
            [[(mt.chan, "The werewolves were: $roles")]]
        m[t.win][r.Win.list_role_p][r.seer] =
            [[(mt.chan, "The seers were: $roles")]]
        m[t.win][r.Win.list_role_p][r.guardian] =
            [[(mt.chan, "The guardian were: $roles")]]
        m[t.win][r.Win.list_role_p][r.angel] =
            [[(mt.chan, "The angels were: $roles")]]
        m[t.win][r.Win.list_role_p][r.traitor] =
            [[(mt.chan, "The traitors were: $roles")]]

        ### MISC MESSAGES ###
        m[t.misc][r.Misc.help][r.noone] =
            [[(mt.notice_p, "To start of a game of Werewolf type: !"+
                            self.commands[Command.start]),
              (mt.notice_p, "To join a running game, while joins are being "+
                            "accepted, type: !"+
                            self.commands[Command.join]),
              (mt.notice_p, "While a game is running and talking is "+
                            "allowed, to name a random player type: !"
                            self.commands[Command.randplayer]),
              (mt.notice_p, "The rest of the commands will be explained "+
                            "in the game.")]]
        m[t.misc][r.Misc.randplayer][r.noone] =
            [[(mt.chan, "The random player is: $target")]]
        m[t.misc][r.Misc.not_player][r.noone] =
            [[(mt.notice_p, "Sorry, you aren't a player of the current game. "+
                            "Join the next game to be part of the fun!")]]
        m[t.misc][r.Misc.dead][r.noone] =
            [[(mt.notice_p, "Sorry, the dead can't do anything.")]]

