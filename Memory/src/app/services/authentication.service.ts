import { Injectable } from "@angular/core";
import { LoginButComponent } from "../login-but/login-but.component";
import { HttpClient } from "@angular/common/http";

import * as moment from "moment";

@Injectable({
  providedIn: "root"
})
export class AuthenticationService {
  constructor(private http: HttpClient) {}

  login(username: string, password: string) {
    return this.http
      .post<any>("http://localhost:5000/api/login", {
        name: username,
        password: password
      })
      .subscribe(
        val => {
          console.log("Test POST succesfull", val);
          this.testSession(val);
          // this.isLoggedIn();
        },
        response => {
          console.log("Test POST unsuccesfull", response.error);
        },
        () => {
          console.log("FINISH HIM");
        }
      );
  }

  logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("expirationDate");
  }

  // Jank goes here:
  testSession(value) {
    // const expirationDate = moment().add(value.expiresIn, "seconds");
    const expiration = value.expiresIn;
    const expirationDate = JSON.parse(expiration);
    localStorage.setItem("token", value.token);
    // localStorage.setItem(
    //   "expirationDate",
    //   JSON.stringify(expirationDate.valueOf())
    // );
    localStorage.setItem("expirationDate", expirationDate);
    console.log(localStorage.getItem("token"));
    console.log(localStorage.getItem("expirationDate"));
    // console.log(moment(expirationDate).format("dddd, MMMM Do YYYY, h:mm:ss"));
    this.testExpiration();
  }

  testExpiration() {
    const expiration = localStorage.getItem("expires_at");
    const expiresAt = JSON.parse(expiration);
    return moment(expiresAt);
  }

  isLoggedIn() {
    // if (moment().isBefore(this.testExpiration())) console.log("TRUE");
    return moment().isBefore(this.testExpiration());
  }

  isLoggedOut() {
    // if (!this.isLoggedIn()) console.log("FALSE");
    return !this.isLoggedIn();
  }
}
