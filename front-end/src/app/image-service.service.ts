import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*'
  })
};

@Injectable({
  providedIn: 'root'
})
export class ImageServiceService {

  constructor(private http: HttpClient) { }

  private url = "http://localhost:5000/addImage";

  public postImage(image){
    return this.http.post<any>(this.url, image, httpOptions).toPromise();
  }
  
}
