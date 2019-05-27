import { Component, OnInit } from "@angular/core";
import { GameService } from "src/app/services/game.service";

@Component({
  selector: "config",
  templateUrl: "./config.component.html",
  styleUrls: ["./config.component.css"]
})
export class ConfigComponent implements OnInit {
  character = [
    { char: "!" },
    { char: "@" },
    { char: "#" },
    { char: "$" },
    { char: "%" }
  ];
  size = [{ number: 2 }, { number: 4 }, { number: 6 }];
  constructor(public gameService: GameService) {}

  ngOnInit() {}

  restart() {
    this.gameService.restart();
  }

  changeCharacter(character: string) {
    this.gameService.character = character;
  }

  changeSize(size: number) {
    this.gameService.size = size;
  }
}
