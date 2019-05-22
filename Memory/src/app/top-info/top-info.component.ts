import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-top-info',
  templateUrl: './top-info.component.html',
  styleUrls: ['./top-info.component.css']
})
export class TopInfoComponent implements OnInit {

  startTijd;
  totaalTijd = 0;
  aantalTijden = 0;
  constructor() { }

  ngOnInit() {
  }

  checkStarttijd() {

    if (this.startTijd == undefined) {
      this.startTijd = this.getSeconds();
    }
    //setTimeout(this.tijdBijhouden, 500);
  }

  // setTijden() {
  //   // bereken de verlopen tijd, de gemiddlede tijd en het verschil tussen
  //  // de huidige speeltijd en de gemiddelde tijd en vul de elementen in de HTML.
  //  // Vul ook het aantal gevonden kaarten
  //  let timePassed = (typeof this.startTijd === "undefined") ? 0 : getSeconds() - this.startTijd;
  //  document.getElementById("tijd").innerHTML = timePassed
  //
  //  averageTime = (aantalTijden === 0) ? 0 : Math.round(totaalTijd / aantalTijden)
  //  timeDifference = (typeof startTijd === "undefined") ? 0 : timePassed - averageTime
  //
  //  uhmString = (timeDifference >= 0) ? "+" : "-"
  //  document.getElementById("gemiddeld").innerHTML = averageTime + " s" + "( " + uhmString + timeDifference + ")"
  //
  //  numberOfCardsFound = (isNaN(numberOfCards - numberOfCardsLeft)) ? 0 : (numberOfCards - numberOfCardsLeft) / 2;
  //  document.getElementById("gevonden").innerHTML = numberOfCardsFound
  // }

  getSeconds() {
    // Een functie om de Systeemtijd in seconden in plaats van miliseconden
    // op te halen. Altijd handig.
    return Math.round(new Date().getTime() / 1000)
  }


  // tijdBijhouden() {
  //   if (numberOfCardsLeft == 0) {
  //     endGame();
  //   } else {
  //     this.setTijden();
  //     // Roep hier deze functie over 500 miliseconden opnieuw aan
  //     let intervalID = setInterval(this.tijdBijhouden, 500)
  //   }
  // }

}
