
using System;
using System.Linq;
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
            .OrderBy(type => type.Namespace)
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
                    Content = form.Name,
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
}
