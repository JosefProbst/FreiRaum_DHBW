import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RoomFinderComponent } from './room-finder.component';

describe('RoomFinderComponent', () => {
  let component: RoomFinderComponent;
  let fixture: ComponentFixture<RoomFinderComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RoomFinderComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RoomFinderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
