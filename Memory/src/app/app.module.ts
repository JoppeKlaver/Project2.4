import { BrowserModule } from "@angular/platform-browser";
import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import { NgModule } from "@angular/core";
import { NgbModule } from "@ng-bootstrap/ng-bootstrap";
import { HttpClientModule } from "@angular/common/http";
// import { JwtModule} from "@auth0/angular-jwt";

import { AppComponent } from "./app.component";
import { PlayingFieldModule } from "./playing-field/playing-field.module";
import { HeaderModule } from "./header/header.module";
import { SidebarModule } from "./sidebar/sidebar.module";
import { LoginButComponent } from './login-but/login-but.component';
import { AppRoutingModule } from './app-routing.module';

@NgModule({
  declarations: [AppComponent, LoginButComponent],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    PlayingFieldModule,
    HeaderModule,
    SidebarModule,
    NgbModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {}
