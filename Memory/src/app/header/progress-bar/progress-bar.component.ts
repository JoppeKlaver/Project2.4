import { Component, OnInit } from "@angular/core";

@Component({
  selector: "progress-bar",
  templateUrl: "./progress-bar.component.html",
  styleUrls: ["./progress-bar.component.css"]
})
export class ProgressBarComponent implements OnInit {
  constructor() {}

  public columns;

  public ngOnInit(): void {
    let percent = 0;
    const intervalId = setInterval(() => {
      this.setProgressbarWidth(percent);
      percent++;
      // percent = getNewPercentValue(percent);
      if (percent > 100) {
        clearInterval(intervalId);
      }
    }, 500);
  }

  public setProgressbarWidth(percent) {
    this.columns = percent + "*," + (100 - percent) + "*";
  }
}
