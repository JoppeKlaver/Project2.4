import { Component, OnInit } from "@angular/core";

@Component({
  selector: "progress-bar",
  templateUrl: "./progress-bar.component.html",
  styleUrls: ["./progress-bar.component.css"]
})
export class ProgressBarComponent implements OnInit {

  interval;
  barValue = 0;

  constructor() {}

  ngOnInit(): void {

  }

  showTime() {
    if(this.barValue <= 100) {
      this.interval = setInterval(() => {
        this.barValue += 1;
      }, 30);
    }
  }

  clearBar() {
    clearInterval(this.interval)
    this.barValue = 0;
  }

}
