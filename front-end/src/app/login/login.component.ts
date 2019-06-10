import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ActivatedRoute } from "@angular/router";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.sass']
})
export class LoginComponent implements OnInit {

  constructor(private router: Router,private route: ActivatedRoute) { }

  user:string;

  ngOnInit() {
    this.user = this.route.snapshot.paramMap.get("id");
    localStorage.setItem("user",this.user);
    this.router.navigate(["/upload"]);
  }

}
