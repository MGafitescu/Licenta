import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {HomeComponent} from '../app/home/home.component'
import {LoginComponent} from '../app/login/login.component'
import {ImageUploadComponent} from '../app/image-upload/image-upload.component'

const routes: Routes = [
  { path: 'home', component: HomeComponent},
  { path: 'login/:id', component: LoginComponent},
  { path: 'upload', component:ImageUploadComponent},
  { path: '', redirectTo: '/home',pathMatch: 'full'}
];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
