import { Client } from 'boardgame.io/client';
import { Debug } from 'boardgame.io/debug';

import { TicTacToe } from './Game.js';

class TicTacToeClient {
    constructor() {
        this.client = Client({
            game: TicTacToe, debug: { impl: Debug },
        });
        this.client.start();
    }
}

const app = new TicTacToeClient();
