
using System;
using System.Linq;
using System.Text.RegularExpressions;
using Avalonia;
using Avalonia.Controls;
using Avalonia.Layout;
using Avalonia.Media;

namespace DersUygulamalari;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();

        var forms = typeof(MainWindow).Assembly.GetTypes()
            .Where(type =>
                type.Namespace != null &&
                type.Namespace.StartsWith("DersUygulamalari.Hafta") &&
                typeof(Window).IsAssignableFrom(type) &&
                !type.IsAbstract &&
                type.GetConstructor(Type.EmptyTypes) != null)
            .OrderBy(type => TrailingNumber(type.Namespace!))
            .ThenBy(type => FormNumber(type.Name))
            .ThenBy(type => type.Name);

        foreach (var week in forms.GroupBy(type => type.Namespace!))
        {
            FormsPanel.Children.Add(new TextBlock
            {
                Text = week.Key.Split('.').Last(),
                FontSize = 20,
                FontWeight = FontWeight.Bold,
                Margin = new Thickness(0, 15, 0, 5)
            });

            var wrapPanel = new WrapPanel
            {
                Orientation = Orientation.Horizontal
            };

            foreach (var form in week)
            {
                var button = new Button
                {
                    // TextBlock: düz metin olarak verilen "_" erişim tuşu sayılıp gizlenir.
                    Content = new TextBlock { Text = ButtonText(form.Name) },
                    MinWidth = 130,
                    Margin = new Thickness(0, 0, 8, 8)
                };

                button.Click += (_, _) =>
                {
                    if (Activator.CreateInstance(form) is Window window)
                    {
                        window.Show();
                    }
                };

                wrapPanel.Children.Add(button);
            }

            FormsPanel.Children.Add(wrapPanel);
        }
    }

    // "Form1_RichTextBoxOzellikleri" -> "1 - RichTextBoxOzellikleri", "Form4" -> "4"
    private static string ButtonText(string name)
    {
        var match = Regex.Match(name, @"^Form(\d+)(?:_(.+))?$");
        if (!match.Success)
            return name;
        return match.Groups[2].Success
            ? $"{match.Groups[1].Value} - {match.Groups[2].Value}"
            : match.Groups[1].Value;
    }

    // Form10'un Form2'den önce gelmemesi için sayıya göre sıralanır.
    private static int FormNumber(string name)
    {
        var match = Regex.Match(name, @"^Form(\d+)");
        return match.Success ? int.Parse(match.Groups[1].Value) : int.MaxValue;
    }

    private static int TrailingNumber(string text)
    {
        var match = Regex.Match(text, @"(\d+)$");
        return match.Success ? int.Parse(match.Groups[1].Value) : int.MaxValue;
    }
}
