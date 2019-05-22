import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-new-game',
  templateUrl: './new-game.component.html',
  styleUrls: ['./new-game.component.css']
})
export class NewGameComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

  newGame(){
    // TODO: reset timers, create new playingfield
    // TODO: update top5
  }

  updateTopScores(){
    
  }
}
