import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs/internal/Observable';
import {environment} from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class FlickrauthService {

  constructor(private http: HttpClient) { }


}
