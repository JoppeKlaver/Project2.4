import { Component, OnInit } from '@angular/core';

import { Player } from '../player'

@Component({
  selector: 'app-top5',
  templateUrl: './top5.component.html',
  styleUrls: ['./top5.component.css']
})
export class Top5Component implements OnInit {

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

  constructor() { }

  ngOnInit() {
  }

}
