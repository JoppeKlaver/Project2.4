import { Injectable } from "@angular/core";

@Injectable({
  providedIn: "root"
})
export class GameService {
  playingField = { Rows: [] };
  size: number;

  inactiveColour = "#f73333";
  activeColour = "#3444bc";
  foundColour = "#0cff00";

  mode: string;

  cards = [];
  character: string;

  firstCard: number;
  secondCard: number;
  temporaryFirstCard: any;
  temporarySecondCard: any;

  gameTimer;
  displayTimer;

  timeToDisplay: number;
  timePassed: number;
  numberOfPairsFound: number;

  topScores = [];
  averageGameTime: number;

  constructor() {
    this.timeToDisplay = 3;
    this.timePassed = 0;
    this.numberOfPairsFound = 0;
    this.character = "*";
    this.size = 6;
    this.averageGameTime = 0;
    this.generateBoard();
    console.log(this.playingField);
    console.log(this.cards);
  }

  generateBoard() {
    let counter = 0;
    var hiddenCharacter = this.nextLetter(this.size);

    for (let row = 0; row < this.size; row++) {
      this.playingField.Rows.push({ cards: [] });
      for (let column = 0; column < this.size; column++) {
        this.playingField.Rows[row].cards.push(counter);
        this.cards.push(hiddenCharacter());
        counter++;
      }
    }
  }

  restart() {
    clearInterval(this.gameTimer);
    clearInterval(this.displayTimer);
    this.timeToDisplay = 3;
    this.timePassed = 0;
    this.numberOfPairsFound = 0;
    this.cards = [];
    this.playingField = { Rows: [] };
    this.gameTimer = undefined;
    this.displayTimer = undefined;
    this.firstCard = undefined;
    this.secondCard = undefined;
    this.temporaryFirstCard = undefined;
    this.temporarySecondCard = undefined;
    this.generateBoard();
  }

  startTime() {
    if (!this.gameTimer) {
      this.gameTimer = setInterval(() => {
        this.timePassed++;
      }, 1000);
    }
  }

  shuffle(Array) {
    var currentIndex = Array.length,
      temporaryValue,
      randomIndex;
    // While there remain elements to shuffle...
    while (0 !== currentIndex) {
      // Pick a remaining element...
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex -= 1;
      // And swap it with the current element.
      temporaryValue = Array[currentIndex];
      Array[currentIndex] = Array[randomIndex];
      Array[randomIndex] = temporaryValue;
    }
    return Array;
  }

  nextLetter = function(size) {
    var letterArray = "AABBCCDDEEFFGGHHIIJJKKLLMMNNOOPPQQRRSSTTUUVVWWXXYYZZ"
      .substring(0, size * size)
      .split("");
    var idx = 0;
    letterArray = this.shuffle(letterArray);
    return function() {
      var letter = letterArray[idx++];
      return letter;
    };
  };
}
