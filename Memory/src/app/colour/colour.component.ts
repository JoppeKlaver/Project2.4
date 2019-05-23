import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-colour',
  templateUrl: './colour.component.html',
  styleUrls: ['./colour.component.css']
})
export class ColourComponent implements OnInit {
  inactiveColour = "#f73333";
  activeColour = "#3444bc";
  foundColour = "#0cff00";

  constructor() { }

  ngOnInit() {
  }

  changeInactiveColour(event: any){
    this.inactiveColour = event.target.value;
  }

  changeActiveColour(event: any){
    this.activeColour = event.target.value;
  }

  changeFoundColour(event: any){
    this.foundColour = event.target.value;
  }

}
