import { Component, OnInit } from '@angular/core';
import { GameService } from 'src/app/services/game.service';

@Component({
  selector: 'config',
  templateUrl: './config.component.html',
  styleUrls: ['./config.component.css']
})
export class ConfigComponent implements OnInit {
  character = [ {char: "*"},
              {char: "#"},
              {char: "$"},
              {char: "%"},
              {char: "X"}];

  size = [{number: 6},
          {number: 4},
          {number: 2}];

  constructor(public gameService: GameService) {}

  ngOnInit() {
  }
}
