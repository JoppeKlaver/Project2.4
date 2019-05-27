import { Component, OnInit } from "@angular/core";
import { GameService } from "src/app/services/game.service";

@Component({
  selector: "card",
  templateUrl: "./card.component.html",
  styleUrls: ["./card.component.css"]
})
export class CardComponent implements OnInit {
  displayTimer: any;

  constructor(public gameService: GameService) {}

  ngOnInit() {
    this.updateAverageGameTime();
  }

  cardClicked(event: {
    target: { id: any; className: string; innerText: any };
  }) {
    let card = event.target.id;

    if (event.target.className == "inactive") {
      if (
        this.gameService.firstCard == undefined &&
        this.gameService.secondCard == undefined
      ) {
        this.gameService.temporaryFirstCard = event.target;
        event.target.className = "active";
        this.gameService.firstCard = card;

        let character = this.gameService.cards[card];
        event.target.innerText = character;
        this.gameService.startTime();
      } else if (
        this.gameService.firstCard != undefined &&
        this.gameService.secondCard == undefined
      ) {
        this.gameService.temporarySecondCard = event.target;
        event.target.className = "active";
        this.gameService.secondCard = card;
        let character = this.gameService.cards[card];
        event.target.innerText = character;
        this.compareCards(
          this.gameService.temporaryFirstCard,
          this.gameService.temporarySecondCard
        );
      } else if (
        this.gameService.firstCard != undefined &&
        this.gameService.secondCard != undefined
      ) {
        clearInterval(this.gameService.displayTimer);
        this.deactivateCards();
        this.cardClicked(event);
      }
    }
  }

  compareCards(card1, card2) {
    if (card1.innerText == card2.innerText) {
      card1.className = "found";
      card2.className = "found";
      this.gameService.numberOfPairsFound++;
      this.gameService.firstCard = undefined;
      this.gameService.secondCard = undefined;
      this.checkIfGameOver();
    } else {
      this.displayTimerStart();
    }
  }

  displayTimerStart() {
    this.gameService.displayTimer = setInterval(() => {
      if (this.gameService.timeToDisplay == 0) {
        clearInterval(this.gameService.displayTimer);
        this.gameService.timeToDisplay = 3;
        this.deactivateCards();
      } else {
        this.gameService.timeToDisplay--;
      }
    }, 1000);
  }

  deactivateCards() {
    this.gameService.temporaryFirstCard.innerText = this.gameService.character;
    this.gameService.temporarySecondCard.innerText = this.gameService.character;
    this.gameService.temporaryFirstCard.className = "inactive";
    this.gameService.temporarySecondCard.className = "inactive";
    this.gameService.firstCard = undefined;
    this.gameService.secondCard = undefined;
    this.gameService.displayTimer = undefined;
  }

  checkIfGameOver() {
    if (
      this.gameService.numberOfPairsFound ==
      this.gameService.cards.length / 2
    ) {
      clearInterval(this.gameService.gameTimer);
      let name = prompt("Who am I?!");
      let newScore = {
        name: name,
        time: this.gameService.timePassed
      };

      this.updateScores(newScore);
      console.log(this.gameService.topScores);
    }
  }

  updateScores(newScore) {
    if (this.gameService.topScores.length >= 5) {
      this.gameService.topScores.pop();
    }
    this.gameService.topScores.push(newScore);
    this.updateAverageGameTime();
    if (this.gameService.topScores.length > 1) {
      this.gameService.topScores.sort((a, b) => {
        return a.time - b.time;
      });
    }
  }

  updateAverageGameTime() {
    let totalTime = 0;
    let numberOfTimes = this.gameService.topScores.length;

    this.gameService.topScores.forEach(function(score) {
      totalTime += score.time;
    });
    this.gameService.averageGameTime = Math.floor(totalTime / numberOfTimes);
  }
}
