import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
import os

CHARTS_DIR = "charts"
os.makedirs(CHARTS_DIR, exist_ok=True)

def parse_metric_value(metric_str):
    if isinstance(metric_str, (int, float)):
        return float(metric_str)

    if isinstance(metric_str, str):
        parts = metric_str.strip().split()
        if len(parts) >= 1:
            try:
                return float(parts[0])
            except ValueError:
                pass
        try:
            return float(metric_str)
        except ValueError:
            return 0
    return 0


def get_metric_info(metric_name):
    metrics_info = {
        'LCP': {
            'full_name': 'Largest Contentful Paint',
            'description': 'Время загрузки основного контента',
            'unit': 'секунды',
            'good': 2.5,
            'poor': 4.0,
            'better': 'меньше',
            'format': '{:.1f} с'
        },
        'FCP': {
            'full_name': 'First Contentful Paint',
            'description': 'Время первого появления контента',
            'unit': 'секунды',
            'good': 1.8,
            'poor': 3.0,
            'better': 'меньше',
            'format': '{:.1f} с'
        },
        'CLS': {
            'full_name': 'Cumulative Layout Shift',
            'description': 'Визуальная стабильность',
            'unit': 'коэффициент',
            'good': 0.1,
            'poor': 0.25,
            'better': 'меньше',
            'format': '{:.3f}'
        },
        'TBT': {
            'full_name': 'Total Blocking Time',
            'description': 'Время блокировки основного потока',
            'unit': 'миллисекунды',
            'good': 200,
            'poor': 600,
            'better': 'меньше',
            'format': '{:.0f} мс'
        },
        'SpeedIndex': {
            'full_name': 'Speed Index',
            'description': 'Скорость отображения контента',
            'unit': 'секунды',
            'good': 3.4,
            'poor': 5.8,
            'better': 'меньше',
            'format': '{:.1f} с'
        }
    }
    return metrics_info.get(metric_name, {
        'full_name': metric_name,
        'description': '',
        'unit': '',
        'good': 0,
        'poor': 0,
        'better': 'меньше',
        'format': '{:.2f}'
    })


def get_metric_status(value, metric_name):
    info = get_metric_info(metric_name)
    if value <= info['good']:
        return 'good'
    elif value <= info['poor']:
        return 'needs-improvement'
    else:
        return 'poor'


def create_individual_metric_chart(metric_name, value, score):
    info = get_metric_info(metric_name)
    status = get_metric_status(value, metric_name)

    colors = {
        'good': '#4CAF50',
        'needs-improvement': '#FFC107',
        'poor': '#F44336'
    }

    fig, ax = plt.subplots(1, 1, figsize=(8, 4))

    max_value = max(value, info['poor'] * 1.5)

    ax.barh([0], [max_value], color='#E0E0E0', alpha=0.3, height=0.3)

    ax.axvline(x=info['good'], color='#4CAF50', linestyle='--', linewidth=2, alpha=0.8,
                label=f'Хорошо (≤{info["good"]})')
    ax.axvline(x=info['poor'], color='#F44336', linestyle='--', linewidth=2, alpha=0.8,
                label=f'Плохо (≥{info["poor"]})')

    bar = ax.barh([0], [value], color=colors[status], height=0.3, alpha=0.8)

    if value > max_value * 0.7:
        ax.text(value - max_value * 0.05, 0, info['format'].format(value),
                 ha='right', va='center', fontweight='bold', color='white')
    else:  # Если значение слева
        ax.text(value + max_value * 0.02, 0, info['format'].format(value),
                 ha='left', va='center', fontweight='bold', color='black')

    ax.set_xlim(0, max_value)
    ax.set_yticks([])
    ax.set_xlabel(f'Значение ({info["unit"]})')
    ax.set_title(f'{metric_name}: {info["full_name"]}', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(axis='x', alpha=0.3)

    ax.text(0.02, 0.95, info['description'], transform=ax.transAxes,
             fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    return fig


def create_metrics_summary_chart(metrics, score):
    metric_names = list(metrics.keys())

    fig, axes = plt.subplots(6, 1, figsize=(10, 14))

    for idx, metric_name in enumerate(metric_names):
        value = parse_metric_value(metrics[metric_name])
        info = get_metric_info(metric_name)
        status = get_metric_status(value, metric_name)

        colors = {
            'good': '#4CAF50',
            'needs-improvement': '#FFC107',
            'poor': '#F44336'
        }

        ax = axes[idx]

        max_value = max(value, info['poor'] * 1.5)

        ax.barh([0], [max_value], color='#E0E0E0', alpha=0.3, height=0.4)

        ax.axvline(x=info['good'], color='#4CAF50', linestyle='--', linewidth=2, alpha=0.8)
        ax.axvline(x=info['poor'], color='#F44336', linestyle='--', linewidth=2, alpha=0.8)

        bar = ax.barh([0], [value], color=colors[status], height=0.4, alpha=0.8)

        if value > (max_value * 0.7):
            ax.text(value - max_value * 0.05, 0, info['format'].format(value),
                    ha='right', va='center', fontweight='bold', color='white')
        else:
            ax.text(value + max_value * 0.02, 0, info['format'].format(value),
                    ha='left', va='center', fontweight='bold', color='black')

        ax.set_xlim(0, max_value)
        ax.set_yticks([])
        ax.set_ylabel(metric_name, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)

        ax.text(0.98, 0.5, f'Хорошо: ≤{info["good"]} | Плохо: ≥{info["poor"]}',
                transform=ax.transAxes, ha='right', va='center',
                fontsize=8, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        ax.text(0.02, -0.6, info['description'], transform=ax.transAxes,
                fontsize=7, alpha=0.7)

    ax_score = axes[-1]
    ax_score.barh(['Performance Score'], [score], color='#2196F3', alpha=0.8, height=0.4)
    ax_score.set_xlim(0, 100)

    if score > 50:
        ax_score.text(score / 2, 0, f'{score:.1f}', ha='center', va='center',
                      fontweight='bold', color='white')
    else:
        ax_score.text(score + 5, 0, f'{score:.1f}', ha='left', va='center',
                      fontweight='bold')

    ax_score.set_yticks([])
    ax_score.set_xlabel('Оценка производительности', fontweight='bold')
    ax_score.grid(axis='x', alpha=0.3)

    ax_score.text(0.98, 0.5, 'Хорошо: ≥90 | Плохо: ≤50',
                  transform=ax_score.transAxes, ha='right', va='center',
                  fontsize=8, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    fig.suptitle('Core Web Vitals Анализ', fontsize=16, fontweight='bold', y=0.98)

    plt.tight_layout()
    return fig


def save_chart(fig, filename_prefix):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.png"
    filepath = os.path.join(CHARTS_DIR, filename)

    fig.savefig(filepath, dpi=100, bbox_inches='tight')
    plt.close(fig)

    return filepath


def generate_visualization(metrics, score):
    parsed_metrics = {}
    for key, value in metrics.items():
        parsed_metrics[key] = parse_metric_value(value)

    chart_paths = {}

    for metric_name, metric_value in parsed_metrics.items():
        fig = create_individual_metric_chart(metric_name, metric_value, score)
        chart_paths[f"{metric_name.lower()}_chart"] = save_chart(fig, f"{metric_name.lower()}_chart")

    fig_summary = create_metrics_summary_chart(metrics, score)
    chart_paths["summary_chart"] = save_chart(fig_summary, "summary_chart")

    return {
        "charts": chart_paths
    }