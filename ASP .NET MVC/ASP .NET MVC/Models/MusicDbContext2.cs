using System;
using System.Collections.Generic;
using System.Data.Entity;
using System.Linq;
using System.Web;

namespace ASP.NET_MVC.Models
{
    public class MusicDbContext2 : DbContext
    {
        public DbSet<Song> Songs { get; set; } 
        public DbSet<Genre> Genres { get; set; }
    }
}