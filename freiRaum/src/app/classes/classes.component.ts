import { Component, OnInit } from '@angular/core';
import { Class } from '../models/class';
import { HttpService } from '../http.service';

@Component({
  selector: 'app-classes',
  templateUrl: './classes.component.html',
  styleUrls: ['./classes.component.css']
})

// hier wird eine Liste aller Kurse angezeigt, sortiert nach deren Kurskategorie
export class ClassesComponent implements OnInit {
  classes: Class[];
  categories: string[];

  constructor(
    private httpService: HttpService
  ) { }

  // beim Laden der Komponente werden alle Kurse von der API abgerufen
  ngOnInit() {
    this.httpService.getClasses()
      .subscribe(
        value => this.classes = value,
        error1 => console.log(error1),
        () => this.getCategories()
      );
  }

  // holt alle Kategorien aus allen Kursen
  getCategories(): void {
    const cats = [];
    for (const c of this.classes) {
      cats.push(c.category);
    }
    // new Set entfernt Duplikate
    this.categories = Array.from(new Set(cats));
  }
}
