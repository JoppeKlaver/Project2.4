import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ConfigComponent } from './config/config.component';
import { ScoresComponent } from './scores/scores.component';
import { FormsModule } from '@angular/forms';

@NgModule({
  declarations: [ConfigComponent, ScoresComponent],
  imports: [
    CommonModule,
    FormsModule
  ],
  exports: [ConfigComponent, ScoresComponent],
})
export class SidebarModule { }
