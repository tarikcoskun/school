using System;
using Avalonia.Controls;
using Avalonia.Interactivity;

namespace DersUygulamalari.Hafta7;

// textBox1'deki yılın her ayında kaç hafta sonu günü olduğunu listBox1'e yazar, en çok olan ayı seçili gösterir.
public partial class Form2_EnCokHaftaSonuOlanAy : Window
{
    public Form2_EnCokHaftaSonuOlanAy()
    {
        InitializeComponent();
    }

    private void Button1_Click(object sender, RoutedEventArgs e)
    {
        listBox1.Items.Clear();

        int yil = Convert.ToInt32(textBox1.Text);

        int en_fazla_haftasonu_iceren_ay = -1;
        int en_fazla_haftasonu_sayisi = 0;
        int bu_ayki_haftasonu_sayisi = 0;

        for (int ay = 1; ay < 13; ay++)
        {
            for (int gun = 1; gun < DateTime.DaysInMonth(yil, ay) + 1; gun++)
            {
                DateTime tarih = new DateTime(yil, ay, gun);

                if (tarih.DayOfWeek == DayOfWeek.Saturday || tarih.DayOfWeek == DayOfWeek.Sunday)
                {
                    bu_ayki_haftasonu_sayisi++;
                }
            }

            if (bu_ayki_haftasonu_sayisi > en_fazla_haftasonu_sayisi)
            {
                en_fazla_haftasonu_sayisi = bu_ayki_haftasonu_sayisi;
                en_fazla_haftasonu_iceren_ay = ay;
            }

            listBox1.Items.Add(new DateTime(yil, ay, 1).ToString("MMMM") + " - " + bu_ayki_haftasonu_sayisi);

            bu_ayki_haftasonu_sayisi = 0;
        }

        listBox1.SelectedItems?.Add(listBox1.Items.GetAt(en_fazla_haftasonu_iceren_ay - 1));
    }
}
