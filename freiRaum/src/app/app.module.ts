import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MaterialModule } from './material.module';
import { FlexLayoutModule } from '@angular/flex-layout';
import { HttpClientModule } from '@angular/common/http';
import { MAT_DIALOG_DEFAULT_OPTIONS, MAT_DATE_LOCALE, DateAdapter } from '@angular/material';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ScheduleModule } from 'primeng/schedule';
import { MatNativeDateModule } from '@angular/material';

import { AppComponent } from './app.component';
import { ClassesComponent } from './classes/classes.component';
import { ClassComponent } from './class/class.component';
import { AppRoutingModule } from './app-routing.module';
import { WelcomeComponent } from './welcome/welcome.component';
import { RoomsComponent, RoomsDialogComponent} from './rooms/rooms.component';
import { RoomComponent } from './room/room.component';
import { RoomFinderComponent, RoomFinderDialogComponent } from './room-finder/room-finder.component';
import { RoomFinderResultsComponent, RoomsFinderResultsDialogComponent } from './room-finder-results/room-finder-results.component';
import { CustomDateAdapter } from './room-finder/room-finder.component';
import { PageNotFoundComponent } from './not-found.component';


@NgModule({
  declarations: [
    AppComponent,
    ClassesComponent,
    ClassComponent,
    WelcomeComponent,
    RoomsComponent,
    RoomsDialogComponent,
    RoomComponent,
    RoomFinderComponent,
    RoomFinderDialogComponent,
    RoomFinderResultsComponent,
    RoomsFinderResultsDialogComponent,
    PageNotFoundComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    MaterialModule,
    FlexLayoutModule,
    HttpClientModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    ScheduleModule,
    MatNativeDateModule
  ],
  entryComponents: [RoomsDialogComponent, RoomsFinderResultsDialogComponent, RoomFinderDialogComponent],
  providers: [
    {provide: MAT_DIALOG_DEFAULT_OPTIONS, useValue: {hasBackdrop: true}},
    {provide: MAT_DATE_LOCALE, useValue: 'de-DE'},
    {provide: DateAdapter, useClass: CustomDateAdapter }
    ],
  bootstrap: [AppComponent]
})
export class AppModule { }
