import {Component, Inject, OnInit} from '@angular/core';
import {HttpParams} from '@angular/common/http';
import {ActivatedRoute} from '@angular/router';
import {Room} from '../models/room';
import {MAT_DIALOG_DATA, MatDialog} from '@angular/material';
import {Location} from '@angular/common';
import {HttpService} from '../http.service';

@Component({
  selector: 'app-room-finder-results',
  templateUrl: './room-finder-results.component.html',
  styleUrls: ['./room-finder-results.component.css']
})

// hier wird die Suchergebnisliste an Räumen angezeigt, die den eingegebenen Kriterien entsprachen
export class RoomFinderResultsComponent implements OnInit {
  rooms: Room[];
  categories: string[];

  startTime: string;
  endTime: string;
  category: string;

  Params = new HttpParams();

  view = 'normal';

  constructor(
    private route: ActivatedRoute,
    private location: Location,
    private httpService: HttpService,
    public dialog: MatDialog
  ) { }

  // beim Laden der Komponente werden zuerst die QueryParameter ausgelesen, um anschließend an die Parameter-Variable angehängt zu werden
  // dann werden alle Räume von der API abgerufen
  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      this.startTime = params['starttime'];
      this.endTime = params['endtime'];
      this.category = params['category'];
    });

    this.Params = (this.startTime === undefined) ? this.Params : this.Params.append('starttime', this.startTime);
    this.Params = (this.endTime === undefined) ? this.Params : this.Params.append('endtime', this.endTime);
    this.Params = (this.category === undefined) ? this.Params : this.Params.append('category', this.category);

    this.httpService.getResults(this.Params)
      .subscribe(
        value => this.rooms = value,
        () => this.view = 'failure',
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
    this.dialog.open(RoomsFinderResultsDialogComponent, {
      width: '330px',
      // übergibt Raumdaten an den Konstruktor der Modal Komponente
      data: { room }
    });
  }

  // führt zur vorherigen Komponente zurück
  goBack(): void {
    this.location.back();
  }
}

// Deklariert die Modal Komponente
@Component({
  selector: 'app-rooms-finder-results-dialog',
  templateUrl: 'rooms-finder-results-dialog.html',
})
export class RoomsFinderResultsDialogComponent {

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {}
}
