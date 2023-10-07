[33mcommit addbd5d12159bc45ec158c861e3f47315a5769dd[m[33m ([m[1;36mHEAD -> [m[1;32mmain[m[33m, [m[1;31morigin/main[m[33m, [m[1;31morigin/HEAD[m[33m)[m
Author: 1paleking1 <1paleking1@gmail.com>
Date:   Fri Oct 6 20:27:45 2023 +0100

    made the window a modal and am debugging why both windows close at the same time

[33mcommit 57069941ab90cbd86b7966a849c45a681df63191[m
Author: 1paleking1 <1paleking1@gmail.com>
Date:   Fri Oct 6 19:53:17 2023 +0100

    added display board window code used in test file to UI.py

[33mcommit c37367777aba1b7a72baf0d914dd3b5aebb1fdf0[m
Author: 1paleking1 <1paleking1@gmail.com>
Date:   Sun Oct 1 19:26:26 2023 +0100

    added test code to the test.py file for a canvas with a display board

[33mcommit 98a84175d3d3aad5fa006e3c0a2d7624ad26d91d[m
Author: 1paleking1 <1paleking1@gmail.com>
Date:   Sun Oct 1 19:04:29 2023 +0100

    did some tidying up of MCTS code and compacted some of it into two more methods

[33mcommit 0f83a2212a6a710c387cb0b49802fe2a3fadadd6[m
Author: 1paleking1 <1paleking1@gmail.com>
Date:   Sat Sep 30 18:45:17 2023 +0100

    fixed issue where the first two moves in a rollout would be of the same colour and made sure each rollout starts with the right piece

[33mcommit f8bdfd5ba20ead768c1f193706a37e9c3a48fde9[m
Author: 1paleking1 <1paleking1@gmail.com>
Date:   Sat Sep 30 12:21:40 2023 +0100

    fixed an issue in the node expansion method to ensure the right player turn is being used.

[33mcommit 8fc8bd34e503bac7d014d929f81e0af4f1f7eb9a[m
Author: 1paleking1 <1paleking1@gmail.com>
Date:   Sat Sep 30 11:28:36 2023 +0100

    MCTS now pretty much works fully. It will make captures that are good but will be smart and not make captures that don't leave it out on top (because if the opponent captures you back its not always the best). To tweak how good it is I can alter the exploration constant and number of moves per rollout. Need to improve the algorithm in the endgame (potentially with an open book) because it doesn't do too well in tricky situations at the very end of the game

[33mcommit 8bbc6bbc38ce55d270fc207a71ec299521b76f02[m
Author: 1paleking1 <1paleking1@gmail.com>
Date:   Sat Sep 30 10:43:45 2023 +0100

    reverted change so that you can technically rollout terminal states but instead they instantly evaluate to a win/loss

[33mcommit 67c0182118616b604dffdcc6c55f817b1fa13f5a[m
Author: 1paleking1 <1paleking1@gmail.com>
Date:   Fri Sep 29 22:54:39 2023 +0100

    added a tree depth attribute to each node

[33mcommit 7ff8042db1b0329a613984574e70b61ba3b81f9b[m
Author: 1paleking1 <1paleking1@gmail.com>
Date:   Fri Sep 29 21:43:09 2023 +0100

    added a check in the selection stage to prevent the selection of terminal states

[33mcommit e2ca52876d0e064cda9988c0885c0a6dffe73a46[m
Author: 1paleking1 <1paleking1@gmail.com>
Date:   Fri Sep 29 21:32:00 2023 +0100

    fixed an MCTS bug where the game would rollout terminal states when near the end of the match. Fixed by giving terminal states a visited value of math.inf and adding a condition to the UCB1 assignment method

[33mcommit 87a9a6f9267ee9c9b1d2ffc16e946f346d8d7f76[m
Merge: 17bd146 4e95c21
Author: 1paleking1 <1paleking1@gmail.com>
Date:   Tue Sep 19 22:04:27 2023 +0100

    added code to the test file to debug  the MCTS code

[33mcommit 17bd146763322aba92eff3eacb20f93a12d93262[m
Author: 1paleking1 <1paleking1@gmail.com>
Date:   Tue Sep 19 19:30:39 2023 +0100

    MCTS progress --> rollouts now alternate between players and I have seen them end in both wins and losses for the AI. But the AI still only moves the same piece

[33mcommit 4e95c214e12008e7198532def8a9fb0da145482a[m
Author: Sahil <1paleking1@gmail.com>
Date:   Tue Sep 12 12:29:28 2023 +0100

    started adding methods to switch player turn in the MCTS class

[33mcommit 14bbb25d2b2b7b2ea9181ed5737468a09b7f48c1[m
Author: Sahil <1paleking1@gmail.com>
Date:   Tue Sep 12 08:43:50 2023 +0100

    I think I've found the problem. I need to also simulate opponent moves in the rollous and consider moves from the opponents perspective when expanding all possible moves so research this

[33mcommit 9a9f15956e0ecdae33519f8f644a3a5eb523bfbc[m
Author: 1paleking1 <1paleking1@gmail.com>
Date:   Tue Sep 12 08:06:42 2023 +0100

    legal captures can now be detected but overall there are still bugs

[33mcommit 6535cf484c7110c1e615ff9e63a2c36e7552da7d[m
Author: 1paleking1 <1paleking1@gmail.com>
Date:   Mon Sep 11 21:55:44 2023 +0100

    issue diagnosed to be that in a position legal captures are not recognised as possible moves which means the Board class's get_legal_moves method needs fixing

[33mcommit 72ef5eeada900c0ddec735f0bb6f403a278da9fb[m
Author: Sahil <1paleking1@gmail.com>
Date:   Mon Sep 11 09:42:37 2023 +0100

    added an is_hint parameter to Node so that MCTS can be called from the perspective of player 1 for a hint

[33mcommit 6a5c2889589f884a1e9cb8c94360250b36652056[m
Author: Sahil <1paleking1@gmail.com>
Date:   Mon Sep 11 09:39:09 2023 +0100

    MCTS now 'works' but for some reason it only moves the same piece until it is captured so need to debug the code

[33mcommit 33d4a430e7cc2948369f659619b96b8076fd5280[m
Author: 1paleking1 <1paleking1@gmail.com>
Date:   Sun Sep 10 18:01:42 2023 +0100

    added a general AIPlayer class to make get_move an abstract method for AI classes and used the GameTree class in the medium AI's get_move

[33mcommit 9b328bb9124b4307605eb337e54c7082eae80994[m
Author: 1paleking1 <1paleking1@gmail.com>
Date:   Sun Sep 10 17:37:36 2023 +0100

    MCTS classes should be finished although they are untested

[33mcommit a037e7598631138c6a79f38bc6ebf2e6eb8c7bdb[m
Author: 1paleking1 <1paleking1@gmail.com>
Date:   Sun Sep 10 17:11:27 2023 +0100

    wrote the backpropagate and rollout methods of the GameTree class. Now adding a timed iteration so MCTS runs for a set amount of time

[33mcommit 4285081c4780066c80b8f276987b1319cbdf1495[m
Author: 1paleking1 <1paleking1@gmail.com>
Date:   Sat Sep 9 11:52:13 2023 +0100

    wrote the get legal states from a board in the Board class and added it to the MCTS

[33mcommit 6c6a15765456d66677968a34e27dd267111af973[m
Author: Sahil <1paleking1@gmail.com>
Date:   Thu Sep 7 08:37:04 2023 +0100

    made the title bigger

[33mcommit 2bffec1c881ae047a184a146b62ae75d3b98439a[m
Author: 1paleking1 <1paleking1@gmail.com>
Date:   Sat Sep 2 20:33:19 2023 +0100

    made the node expansion method

[33mcommit 7222e47459520274ff8760c7ef09bae91b1cd9ac[m
Author: 1paleking1 <1paleking1@gmail.com>
Date:   Sat Sep 2 17:49:14 2023 +0100

    more work on the tree classes to get a game tree working

[33mcommit acceb04812a87da04167c3f0257c27435695b5b7[m
Author: 1paleking1 <1paleking1@gmail.com>
Date:   Sat Sep 2 17:35:24 2023 +0100

    preliminary work on the tree classes

[33mcommit af50082ee4ff1567f06f714177974cbe77e37c77[m
Author: 1paleking1 <1paleking1@gmail.com>
Date:   Sat Sep 2 16:55:42 2023 +0100

    copied files into stage 5 tree search AI. KNOWN ISSUE TO FIx: another game can't be played after one is completed will fix this

[33mcommit 66f4842bced2a61076ec20134921a565296c77b4[m
Author: 1paleking1 <1paleking1@gmail.com>
Date:   Sat Sep 2 16:39:14 2023 +0100

    new counter images made and put into folders for use later on

[33mcommit 54dbb7532161d9bfc44bbefdfdf4d8cbcd4ca98e[m
Author: 1paleking1 <1paleking1@gmail.com>
Date:   Tue Aug 29 19:21:15 2023 +0100

    working on changing the button piece graphics to include the loops

[33mcommit b04486c14fc621009f0115ed8768c5424fe78e77[m
Merge: 545ae0f e0219b6
Author: 1paleking1 <1paleking1@gmail.com>
Date:   Mon Aug 28 22:20:07 2023 +0100

    improved EasyAI by making it always look for captures first and then making a corner moves only when no captures can be made. Improved the board shuffling function by using a new flattening function for a 2D array in utility_functions

[33mcommit 545ae0fb849de376d1986ae08e86b820cac572c5[m
Author: 1paleking1 <1paleking1@gmail.com>
Date:   Mon Aug 28 22:11:08 2023 +0100

    improved EasyAI to always capture and then make corner move. Improved shuffle to shuffle between rows too 