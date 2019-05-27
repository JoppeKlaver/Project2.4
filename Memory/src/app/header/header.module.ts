import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { HeaderComponent } from "./header/header.component";
import { ProgressBarComponent } from './progress-bar/progress-bar.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {MatProgressBarModule} from '@angular/material/progress-bar';

@NgModule({
  declarations: [HeaderComponent, ProgressBarComponent],
  imports: [CommonModule, BrowserAnimationsModule, MatProgressBarModule],
  exports: [HeaderComponent, ProgressBarComponent],
})
export class HeaderModule {}
