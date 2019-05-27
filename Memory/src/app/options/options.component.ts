import { Component, OnInit } from '@angular/core';
import { TestService } from '../test.service';
import { TimeService } from '../time.service';

@Component({
  selector: 'app-options',
  templateUrl: './options.component.html',
  styleUrls: ['./options.component.css']
})
export class OptionsComponent implements OnInit {
  message:number;
  time:number;
  selectedCharacter: String = "*";
  selectedSize = 6;
  timePlayed = 0;
  timeDifference = 0;
  interval = undefined;
  averageTime = 0;

  character = [ {char: "*"},
                {char: "#"},
                {char: "$"},
                {char: "%"},
                {char: "X"}];

  size = [{number: 6},
          {number: 4},
          {number: 2}];

  constructor(private data: TestService, private timeService: TimeService) {
    this.data.currentMessage.subscribe(message => this.message = message)
    this.timeService.currentMessage.subscribe(message => this.time = message)
  }

  ngOnInit() {
    this.timeDifference = 0 - this.message;
  }


  startTimer(){
    if(!this.interval){
      this.timeDifference = 0 - this.message;
      this.interval = setInterval(() => {
        this.timePlayed += 1;
        this.timeDifference +=1;
        this.timeService.changeMessage(this.timePlayed)
      }, 1000);
    }
  }

  stopTimer(){
    clearInterval(this.interval);
    this.interval = undefined;
    this.timePlayed = 0;
    this.timeService.changeMessage(0);
    this.timeDifference = 0 - this.message;
  }

  selectCharacterHandler(event: any){
    this.selectedCharacter = event.target.value;
  }

  selectSizeHandler(event: any){
    this.selectedSize = event.target.value
  }
}
