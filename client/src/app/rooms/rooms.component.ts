import {Component, OnInit, Inject} from '@angular/core';
import {Room} from '../models/room';
import {MAT_DIALOG_DATA, MatDialog} from '@angular/material';
import {HttpService} from '../http.service';

@Component({
  selector: 'app-rooms',
  templateUrl: './rooms.component.html',
  styleUrls: ['./rooms.component.css']
})

// hier wird eine Liste aller Räume angezeigt, sortiert nach deren Raumkategorie
export class RoomsComponent implements OnInit {
  rooms: Room[];
  categories: string[];

  constructor(
    private httpService: HttpService,
    public dialog: MatDialog
  ) { }

  // beim Laden der Komponente werden alle Räume von der API abgerufen
  ngOnInit() {
    this.httpService.getRooms()
      .subscribe(
        value => this.rooms = value,
        error1 => console.log(error1),
        () => this.getCategories()
      );
  }

  // holt alle Kategorien aus allen Räumen
  getCategories(): void {
    const cats = [];
    for (const c of this.rooms) {
      cats.push(c.category);
    }
    // new Set entfernt Duplikate
    this.categories = Array.from(new Set(cats));
  }

  // öffnet ein Model, um Extra-Informationen über den Raum anzuzeigen
  openDialog(roomId: string): void {
    // sucht den Raum, auf dessen Info-Button geklickt wurde
    const room = this.rooms.find(value => roomId === value.roomId);
    this.dialog.open(RoomsDialogComponent, {
      width: '330px',
      // übergibt Raumdaten an den Konstruktor der Modal Komponente
      data: {room}
    });
  }
}

// Deklariert die Modal Komponente
@Component({
  selector: 'app-rooms-dialog',
  templateUrl: 'rooms-dialog.html',
})
export class RoomsDialogComponent {

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {
  }
}
