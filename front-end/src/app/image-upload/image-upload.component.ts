import { Component, OnInit } from '@angular/core';
import { ImageServiceService } from '../image-service.service'

@Component({
  selector: 'app-image-upload',
  templateUrl: './image-upload.component.html',
  styleUrls: ['./image-upload.component.scss']
})
export class ImageUploadComponent implements OnInit {

  constructor(private imageService: ImageServiceService) { }

  imagePath: string;
  imageUrl: any;
  message: string;
  image: string;
  loading = false;
  result: any;
  selectedOption: string  = 'Profile';
  options: string[] = ['Profile', 'Contacts','Public'];

  ngOnInit() {
  }

  preview(file) {
    if (file.files.length === 0)
      return;

    let fileReader = new FileReader();
    this.imagePath = <string>file.files[0].name;
    fileReader.readAsDataURL(file.files[0]);
    fileReader.onload = () => {
      this.imageUrl = fileReader.result;
    }
    fileReader.onloadend = () => {
      this.image = <string>fileReader.result;
      let reg = new RegExp("^data:image\/[a-zA-Z]+;base64,");
      this.image = this.image.replace(reg, "");

    }
  }


  async upload() {
    this.loading = true;
    let user:string;
    user = localStorage.getItem("user");
    this.result = await this.imageService.postImage({ user: user, name: this.imagePath, file: this.image, option: this.selectedOption });
    this.result = JSON.parse(this.result);
    console.log(this.result);
    this.loading = false;
  }
}
