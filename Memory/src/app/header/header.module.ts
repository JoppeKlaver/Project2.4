import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { HeaderComponent } from "./header/header.component";
import { ProgressBarComponent } from './progress-bar/progress-bar.component';

@NgModule({
  declarations: [HeaderComponent, ProgressBarComponent],
  imports: [CommonModule],
  exports: [HeaderComponent, ProgressBarComponent],
})
export class HeaderModule {}
