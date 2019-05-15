import { TestBed } from '@angular/core/testing';

import { FlickrauthService } from './flickrauth.service';

describe('FlickrauthService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: FlickrauthService = TestBed.get(FlickrauthService);
    expect(service).toBeTruthy();
  });
});
