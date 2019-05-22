import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-options',
  templateUrl: './options.component.html',
  styleUrls: ['./options.component.css']
})
export class OptionsComponent implements OnInit {
  selectedCharacter = "*";
  selectedSize = 6;
  timePlaying = 0;
  timeDifference = 0;
  interval;

  character = [ {char: "*"},
                {char: "#"},
                {char: "$"},
                {char: "%"},
                {char: "X"}];

  size = [{number: 6},
          {number: 4},
          {number: 2}];

  constructor() { }

  ngOnInit() {
  }

  startTimer(){
    if(!this.interval){
      this.interval = setInterval(() => {
        this.timePlaying += 1, this.timeDifference += 1;
      }, 1000);
    }
  }

  stopTimer(){
    clearInterval(this.interval);
    this.interval = undefined;
    this.timeDifference = this.timePlaying - (2*this.timePlaying);
    this.timePlaying = 0;
  }

  selectCharacterHandler(event: any){
    this.selectedCharacter = event.target.value;
  }

  selectSizeHandler(event: any){
    this.selectedSize = event.target.value
  }
}
