import { Component, OnInit } from '@angular/core';
import { TimeService } from '../time.service';

@Component({
  selector: 'app-top-info',
  templateUrl: './top-info.component.html',
  styleUrls: ['./top-info.component.css']
})
export class TopInfoComponent implements OnInit {
  time:number;
  foundCardPairs = 0;
  remainingTime = 3;
  remainingTimeID = undefined;

  constructor(private timeService: TimeService) {
    this.timeService.currentMessage.subscribe(message => this.time = message);
  }

  ngOnInit() {
  }

  startRemainingTime(){
    if(!this.remainingTimeID){
      this.remainingTimeID = setInterval(() => {
        if(this.remainingTime > 0){
          this.remainingTime -= 1;
        } else {
          this.stopRemainingTime();
        }
      }, 1000);
    }
  }

  stopRemainingTime(){
    clearInterval(this.remainingTimeID);
    this.remainingTimeID = undefined;
    this.remainingTime = 3;
  }
}
