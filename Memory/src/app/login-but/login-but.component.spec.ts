import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LoginButComponent } from './login-but.component';

describe('LoginButComponent', () => {
  let component: LoginButComponent;
  let fixture: ComponentFixture<LoginButComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LoginButComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LoginButComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
