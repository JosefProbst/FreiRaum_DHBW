import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { ClassesComponent } from './classes/classes.component';
import { WelcomeComponent } from './welcome/welcome.component';
import { ClassComponent } from './class/class.component';
import {RoomsComponent} from './rooms/rooms.component';
import {RoomComponent} from './room/room.component';
import {RoomFinderComponent} from './room-finder/room-finder.component';
import {RoomFinderResultsComponent} from './room-finder-results/room-finder-results.component';
import {PageNotFoundComponent} from './not-found.component';

const routes: Routes = [
  { path: '', component: WelcomeComponent },
  { path: 'classes', component: ClassesComponent },
  { path: 'classes/:classId', component: ClassComponent },
  { path: 'rooms', component: RoomsComponent },
  { path: 'rooms/:roomId', component: RoomComponent },
  { path: 'roomFinder', component: RoomFinderComponent},
  { path: 'roomFinder/results', component: RoomFinderResultsComponent },
  { path: '**', component: PageNotFoundComponent}
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}
