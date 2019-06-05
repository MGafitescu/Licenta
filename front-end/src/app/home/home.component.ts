import { Component, OnInit } from '@angular/core';
import { FlickrauthService } from '../flickrauth.service'

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  constructor(private flickrauthService: FlickrauthService) { }

  result: any;


  ngOnInit() {
  }

  functie() {
    console.log("AAa");

  }



}
