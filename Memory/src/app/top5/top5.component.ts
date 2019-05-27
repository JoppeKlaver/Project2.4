import { Component, OnInit } from '@angular/core';
import { TestService } from '../test.service';
import { Player } from '../player'

@Component({
  selector: 'app-top5',
  templateUrl: './top5.component.html',
  styleUrls: ['./top5.component.css']
})
export class Top5Component implements OnInit {
  averageTime = 0;
  message:number;

   TOP5: Player[] =  [{
        name: "Barack Obama",
        time: 200
    },
    {
        name: "Bernie Sanders",
        time: 300
    },
    {
        name: "Hillary Clinton",
        time: 400
    },
    {
        name: "Jeb Bush",
        time: 500
    },
    {
        name: "Donald Trump",
        time: 600
    }
]

  constructor(private data: TestService) { }

  ngOnInit() {
    this.data.currentMessage.subscribe(message => this.message = message)
    this.setAverageTime();
  }

  addTopScore(name: string, time: number){
    this.TOP5.push({name: name, time: time})
    this.TOP5.sort(( a, b)=> (a.time > b.time) ? 1 : ((b.time > a.time) ? -1 : 0));
    this.TOP5.length = 5;
    this.setAverageTime();
  }

  setAverageTime(){
    this.averageTime = 0;
    for(let i of this.TOP5){
      this.averageTime += i.time;
    }
    this.averageTime = this.averageTime / this.TOP5.length;
    this.data.changeMessage(this.averageTime)
  }
}
