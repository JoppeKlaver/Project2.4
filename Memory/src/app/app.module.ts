import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { Top5Component } from './top5/top5.component';
import { KleurComponent } from './kleur/kleur.component';
import { ColourComponent } from './colour/colour.component';
import { OptionsComponent } from './options/options.component';
import { NewGameComponent } from './new-game/new-game.component';
import { TopInfoComponent } from './top-info/top-info.component';

@NgModule({
  declarations: [
    AppComponent,
    Top5Component,
    KleurComponent,
    ColourComponent,
    OptionsComponent,
    NewGameComponent,
    TopInfoComponent
  ],
  imports: [
    BrowserModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
