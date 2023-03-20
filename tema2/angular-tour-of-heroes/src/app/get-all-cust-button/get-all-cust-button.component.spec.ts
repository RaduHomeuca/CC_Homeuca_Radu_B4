import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GetAllCustButtonComponent } from './get-all-cust-button.component';

describe('GetAllCustButtonComponent', () => {
  let component: GetAllCustButtonComponent;
  let fixture: ComponentFixture<GetAllCustButtonComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GetAllCustButtonComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GetAllCustButtonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
